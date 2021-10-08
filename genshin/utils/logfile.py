"""Utility functuon for extracting data from logfiles"""
import os
import re
from tempfile import gettempdir
from typing import List, Optional
from urllib.parse import unquote

__all__ = ["get_logfile", "extract_authkey", "get_authkey", "get_banner_ids"]

AUTHKEY_FILE = os.path.join(gettempdir(), "genshinstats_authkey.txt")


def get_logfile() -> Optional[str]:
    """Find and return the Genshin Impact logfile. None if not found."""
    mihoyo_dir = os.path.expanduser("~/AppData/LocalLow/miHoYo/")
    for name in ["Genshin Impact", "原神", "YuanShen"]:
        output_log = os.path.join(mihoyo_dir, name, "output_log.txt")
        if os.path.isfile(output_log):
            return output_log

    return None  # no genshin installation


def _read_logfile(logfile: Optional[str] = None) -> str:
    """Returns the contents of a logfile"""
    logfile = logfile or get_logfile()
    if logfile is None:
        raise FileNotFoundError("No Genshin Installation was found, could not get gacha data.")
    with open(logfile) as file:
        return file.read()


def extract_authkey(string: str) -> Optional[str]:
    """Extracts an authkey from the provided string. Returns None if not found."""
    match = re.search(r"https://.+?authkey=([^&#]+)", string, re.MULTILINE)
    if match is not None:
        return unquote(match.group(1))
    return None


def get_authkey(logfile: str = None) -> str:
    """Gets the query for log requests.

    This will either be done from the logs or from a tempfile.
    """
    # first try the log
    authkey = extract_authkey(_read_logfile(logfile))
    if authkey is not None:
        with open(AUTHKEY_FILE, "w") as file:
            file.write(authkey)
        return authkey

    # otherwise try the tempfile (may be expired!)
    if os.path.isfile(AUTHKEY_FILE):
        with open(AUTHKEY_FILE) as file:
            return file.read()

    raise Exception(
        "No authkey could be found in the logs or in a tempfile. "
        "Open the history in-game first before attempting to request it."
    )


def get_banner_ids(logfile: str = None) -> List[str]:
    """Gets all banner ids from a log file.
    You need to open the details of all banners for this to work.
    """
    log = _read_logfile(logfile)
    ids = re.findall(r"OnGetWebViewPageFinish:https://.+?gacha_id=([^&#]+)", log)
    return list(set(ids))
