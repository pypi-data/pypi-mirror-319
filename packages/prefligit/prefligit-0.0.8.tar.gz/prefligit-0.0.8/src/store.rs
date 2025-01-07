use std::path::{Path, PathBuf};
use std::sync::LazyLock;

use anyhow::Result;
use etcetera::BaseStrategy;
use rusqlite::Connection;
use thiserror::Error;
use tracing::debug;

use crate::config::RemoteRepo;
use crate::env_vars::EnvVars;
use crate::fs::{copy_dir_all, LockedFile};
use crate::git::clone_repo;
use crate::hook::{Hook, Repo};

#[derive(Debug, Error)]
pub enum Error {
    #[error("Home directory not found")]
    HomeNotFound,
    #[error("Local hook {0} does not need env")]
    LocalHookNoNeedEnv(String),
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Fmt(#[from] std::fmt::Error),
    #[error(transparent)]
    DB(#[from] rusqlite::Error),
    #[error(transparent)]
    Repo(#[from] crate::hook::Error),
    #[error(transparent)]
    Git(#[from] crate::git::Error),
}

static STORE_HOME: LazyLock<Option<PathBuf>> = LazyLock::new(|| {
    if let Some(path) = std::env::var_os(EnvVars::PREFLIGIT_HOME) {
        debug!(
            path = %path.to_string_lossy(),
            "Loading store from PREFLIGIT_HOME env var",
        );
        Some(path.into())
    } else {
        etcetera::choose_base_strategy()
            .map(|path| path.cache_dir().join("prefligit"))
            .ok()
    }
});

/// A store for managing repos.
#[derive(Debug)]
pub struct Store {
    path: PathBuf,
    conn: Option<Connection>,
}

impl Store {
    pub fn from_settings() -> Result<Self, Error> {
        Ok(Self::from_path(
            STORE_HOME.as_ref().ok_or(Error::HomeNotFound)?,
        ))
    }

    pub fn from_path(path: impl Into<PathBuf>) -> Self {
        Self {
            path: path.into(),
            conn: None,
        }
    }

    pub fn path(&self) -> &Path {
        self.path.as_ref()
    }

    fn conn(&self) -> &Connection {
        self.conn.as_ref().expect("store not initialized")
    }

    /// Initialize the store.
    pub fn init(self) -> Result<Self, Error> {
        fs_err::create_dir_all(&self.path)?;

        // Write a README file.
        match fs_err::write(
            self.path.join("README"),
            b"This directory is maintained by the pre-commit project.\nLearn more: https://github.com/pre-commit/pre-commit\n",
        ) {
            Ok(()) => (),
            Err(err) if err.kind() == std::io::ErrorKind::AlreadyExists => (),
            Err(err) => return Err(err.into()),
        }

        let _lock = self.lock()?;

        // Init the database.
        let db = self.path.join("db.db");
        let conn = if db.try_exists()? {
            debug!(db = %db.display(), "Opening database");
            Connection::open(&db)?
        } else {
            debug!(db = %db.display(), "Creating database");
            let conn = Connection::open(&db)?;
            conn.execute(
                "CREATE TABLE repos (
                    repo TEXT NOT NULL,
                    ref TEXT NOT NULL,
                    path TEXT NOT NULL,
                    PRIMARY KEY (repo, ref)
                );",
                [],
            )?;
            conn
        };

        Ok(Self {
            conn: Some(conn),
            ..self
        })
    }

    /// List all repos.
    pub fn repos(&self) -> Result<Vec<Repo>, Error> {
        let mut stmt = self.conn().prepare("SELECT repo, ref, path FROM repos")?;

        let rows: Vec<_> = stmt
            .query_map([], |row| {
                let name: String = row.get(0)?;
                let rev: String = row.get(1)?;
                let path: String = row.get(2)?;
                Ok((name, rev, path))
            })?
            .collect::<Result<_, _>>()?;

        // TODO: fix, local repo can also in the store
        rows.into_iter()
            .map(|(url, rev, path)| Repo::remote(&url, &rev, &path).map_err(Error::Repo))
            .collect::<Result<Vec<_>, Error>>()
    }

    // Append dependencies to the repo name as the key.
    fn repo_name(repo: &str, deps: &[String]) -> String {
        let mut name = repo.to_string();
        if !deps.is_empty() {
            name.push(':');
            name.push_str(&deps.join(","));
        }
        name
    }

    fn get_repo(
        &self,
        repo: &str,
        rev: &str,
        deps: &[String],
    ) -> Result<Option<(String, String, String)>, Error> {
        let repo_name = Self::repo_name(repo, deps);

        let mut stmt = self
            .conn()
            .prepare("SELECT repo, ref, path FROM repos WHERE repo = ? AND ref = ?")?;
        let mut rows = stmt.query([repo_name.as_str(), rev])?;
        let Some(row) = rows.next()? else {
            return Ok(None);
        };
        Ok(Some((row.get(0)?, row.get(1)?, row.get(2)?)))
    }

    fn insert_repo(&self, repo: &str, rev: &str, path: &str, deps: &[String]) -> Result<(), Error> {
        let repo_name = Self::repo_name(repo, deps);

        let mut stmt = self
            .conn()
            .prepare("INSERT INTO repos (repo, ref, path) VALUES (?, ?, ?)")?;
        stmt.execute([repo_name.as_str(), rev, path])?;
        Ok(())
    }

    /// Prepare a local repo for a local hook.
    /// All local hooks with same additional dependencies, e.g. no dependencies,
    /// are stored in the same directory (even they use different language).
    pub fn prepare_local_repo(&self, hook: &Hook, deps: &[String]) -> Result<PathBuf, Error> {
        const LOCAL_NAME: &str = "local";
        const LOCAL_REV: &str = "1";

        if hook.language.environment_dir().is_none() {
            return Err(Error::LocalHookNoNeedEnv(hook.id.clone()));
        }

        let path = if let Some((_, _, path)) = self.get_repo(LOCAL_NAME, LOCAL_REV, deps)? {
            path
        } else {
            let temp = tempfile::Builder::new()
                .prefix("repo")
                .keep(true)
                .tempdir_in(&self.path)?;

            let path = temp.path().to_string_lossy().to_string();
            debug!(hook = hook.id, path, "Preparing local repo");
            make_local_repo(LOCAL_NAME, temp.path())?;
            self.insert_repo(LOCAL_NAME, LOCAL_REV, &path, deps)?;
            path
        };

        Ok(PathBuf::from(path))
    }

    /// Clone a remote repo into the store.
    pub async fn prepare_remote_repo(
        &self,
        repo_config: &RemoteRepo,
        deps: &[String],
    ) -> Result<PathBuf, Error> {
        if let Some((_, _, path)) = self.get_repo(
            repo_config.repo.as_str(),
            repo_config.rev.as_str(),
            deps.as_ref(),
        )? {
            return Ok(PathBuf::from(path));
        }

        // Clone and checkout the repo.
        let temp = tempfile::Builder::new()
            .prefix("repo")
            .keep(true)
            .tempdir_in(&self.path)?;
        let path = temp.path().to_string_lossy().to_string();

        if deps.is_empty() {
            debug!(
                target = path,
                repo = format!("{}@{}", repo_config.repo, repo_config.rev),
                "Cloning repo",
            );
            clone_repo(repo_config.repo.as_str(), &repo_config.rev, temp.path()).await?;
        } else {
            // FIXME: Do not copy env dir.
            // TODO: use hardlink?
            // Optimization: This is an optimization from the Python pre-commit implementation.
            // Copy already cloned base remote repo.
            let (_, _, base_repo_path) = self
                .get_repo(repo_config.repo.as_str(), repo_config.rev.as_str(), &[])?
                .expect("base repo should be cloned before");
            debug!(
                source = base_repo_path,
                target = path,
                deps = deps.join(","),
                "Preparing {}@{} by copying",
                repo_config.repo,
                repo_config.rev,
            );
            copy_dir_all(base_repo_path, &path)?;
        }

        self.insert_repo(
            repo_config.repo.as_str(),
            repo_config.rev.as_str(),
            &path,
            deps,
        )?;

        Ok(PathBuf::from(path))
    }

    /// Lock the store.
    pub fn lock(&self) -> Result<LockedFile, std::io::Error> {
        LockedFile::acquire_blocking(self.path.join(".lock"), "store")
    }

    pub async fn lock_async(&self) -> Result<LockedFile, std::io::Error> {
        LockedFile::acquire(self.path.join(".lock"), "store").await
    }

    /// The path to the tool directory in the store.
    pub fn tools_path(&self, tool: ToolBucket) -> PathBuf {
        self.path.join("tools").join(tool.as_str())
    }
}

#[derive(Copy, Clone)]
pub enum ToolBucket {
    Uv,
    Python,
    Node,
}

impl ToolBucket {
    pub fn as_str(&self) -> &str {
        match self {
            ToolBucket::Uv => "uv",
            ToolBucket::Python => "python",
            ToolBucket::Node => "node",
        }
    }
}

// TODO
/// For local repo, creates a dummy package for each supported language, to make
/// the installation code like `pip install .` work.
fn make_local_repo(_repo: &str, path: &Path) -> Result<(), Error> {
    fs_err::create_dir_all(path)?;
    fs_err::File::create(path.join("__init__.py"))?;
    fs_err::write(
        path.join("setup.py"),
        indoc::indoc! {r#"
    from setuptools import setup

    setup(name="pre-commit-placeholder-package", version="0.0.0")
    "#},
    )?;

    Ok(())
}
