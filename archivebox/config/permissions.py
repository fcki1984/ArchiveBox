__package__ = 'archivebox.config'

import os
from pathlib import Path
from contextlib import contextmanager

#############################################################################################

DATA_DIR = Path(os.getcwd())

DATA_DIR_STAT           = Path(DATA_DIR).stat()
DATA_DIR_UID            = DATA_DIR_STAT.st_uid
DATA_DIR_GID            = DATA_DIR_STAT.st_gid
DEFAULT_PUID            = 911
DEFAULT_PGID            = 911
RUNNING_AS_UID          = os.getuid()
RUNNING_AS_GID          = os.getgid()
EUID                    = os.geteuid()
EGID                    = os.getegid()
USER: str               = Path('~').expanduser().resolve().name

IS_ROOT = RUNNING_AS_UID == 0
IN_DOCKER = os.environ.get('IN_DOCKER', False) in ('1', 'true', 'True', 'TRUE', 'yes')

os.environ.setdefault('PUID', str(DATA_DIR_UID or RUNNING_AS_UID or DEFAULT_PUID))
os.environ.setdefault('PGID', str(DATA_DIR_GID or RUNNING_AS_GID or DEFAULT_PGID))

ARCHIVEBOX_USER = int(os.environ['PUID'])
ARCHIVEBOX_GROUP = int(os.environ['PGID'])

#############################################################################################

def drop_privileges():
    """If running as root, drop privileges to the user that owns the data dir (or PUID, or default=911)"""
    
    # always run archivebox as the user that owns the data dir, never as root
    if os.getuid() == 0:
        # drop permissions to the user that owns the data dir / provided PUID
        if os.geteuid() != ARCHIVEBOX_USER:
            os.seteuid(ARCHIVEBOX_USER)
        # if we need sudo (e.g. for installing dependencies) code should use SudoPermissions() context manager to regain root


@contextmanager
def SudoPermission(uid=0, fallback=False):
    """Attempt to run code with sudo permissions for a given user (or root)"""
    
    if os.geteuid() == uid:
        # no need to change effective UID, we are already that user
        yield
        return

    try:
        # change our effective UID to the given UID
        os.seteuid(uid)
    except PermissionError as err:
        if not fallback:
            raise PermissionError(f'Not enough permissions to run code as uid={uid}, please retry with sudo') from err
    try:
        # yield back to the caller so they can run code inside context as root
        yield
    finally:
        # then set effective UID back to DATA_DIR owner
        DATA_DIR_OWNER = DATA_DIR.stat().st_uid
        try:
            os.seteuid(DATA_DIR_OWNER)
        except PermissionError as err:
            if not fallback:
                raise PermissionError(f'Failed to revert uid={uid} back to {DATA_DIR_OWNER} after running code with sudo') from err

