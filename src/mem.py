"""Memory module for KC-NOTIF.

Contains:
    🌟 Get file.
    🌟 Write file.
    🌟 Set up clist.
    🌟 Generate save data.
"""

import json, os
from api import API

# SWITCH TO SQLITE3 .DEV


def get_file(name: str) -> list:
    """Loads file at data/name into memory.

    Args:
        name (str): File name.

    Returns:
        list: json representation of the file.
    """

    try:
        with open(f"data/{name}", "r+") as file:
            return json.loads(list(file)[0])
    except FileNotFoundError:
        write_file(name, [{}])
        return [{}]


def write_file(name: str, content: list) -> None:
    """Writes a json-formatted obj to a file.

    Args:
        name (str): File name.
        content (list): json-formatted contents of the file.

    Returns:
        None
    """
    if not os.path.isdir("data"):
        os.makedirs("data")

    with open(f"data/{name}", "w+") as file:
        file.write(json.dumps(content))


def get_clist(api: API) -> list:
    clist = sorted(
        api.get_creators_list(), key=lambda creator: creator["favorited"], reverse=True
    )
    # write_file("clist", clist)
    return clist


def gen_saved_data(timer: int) -> list:
    saved_data = get_file("saved_data")
    if "timer" not in saved_data[0].keys():
        saved_data[0]["timer"] = timer
        write_file("saved_data", saved_data)
    return saved_data
