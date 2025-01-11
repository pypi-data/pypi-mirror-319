import pathlib

from hyperpocket.repository.lock import LocalLock, GitLock
from hyperpocket.repository.lockfile import Lockfile


def pull(lockfile: Lockfile, urllike: str, git_ref: str):
    path = pathlib.Path(urllike)
    if path.exists():
        lockfile.add_lock(LocalLock(tool_path=str(path)))
    else:
        lockfile.add_lock(GitLock(repository_url=urllike, git_ref=git_ref))
    lockfile.sync(force_update=False)
    lockfile.write()
    
def sync(lockfile: Lockfile, force_update: bool):
    lockfile.sync(force_update=force_update)
    lockfile.write()
