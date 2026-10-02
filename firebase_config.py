import os
import json
import threading
from copy import deepcopy

from dotenv import load_dotenv

load_dotenv()

# ============================================================
# LOCAL DATABASE
# ============================================================
# Temporary replacement for Firebase during local development.
#
# Data is stored in:
#     local_database.json
#
# This keeps the same basic interface that app.py currently
# uses:
#
#     db.reference("/hotel").get()
#     db.reference("/hotel/crisis_active").set(True)
#
# Later, Firebase/Supabase/PostgreSQL can be added without
# changing the frontend structure.
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "local_database.json")

_lock = threading.Lock()


# ============================================================
# DEFAULT DATA
# ============================================================

DEFAULT_DATABASE = {
    "hotel": {
        "crisis_active": False,
        "crisis_type": "",
        "crisis_floor": 0,
        "danger_zones": [],
        "severity": 0,

        # Demo occupants.
        # These can be changed later from the application.
        "persons": {
            "GUEST-001": {
                "name": "Demo Guest",
                "floor": 3,
                "zone": "Room 301",
                "room": "301",
                "role": "guest",
                "special_needs": "none",
                "language": "English"
            },

            "GUEST-002": {
                "name": "Demo Guest 2",
                "floor": 3,
                "zone": "Room 305",
                "room": "305",
                "role": "guest",
                "special_needs": "none",
                "language": "English"
            },

            "GUEST-003": {
                "name": "Demo Guest 3",
                "floor": 2,
                "zone": "Room 204",
                "room": "204",
                "role": "guest",
                "special_needs": "mobility",
                "language": "English"
            },

            "STAFF-001": {
                "name": "Demo Staff",
                "floor": 1,
                "zone": "Reception",
                "room": "Reception",
                "role": "staff",
                "special_needs": "none",
                "language": "English"
            }
        }
    }
}


# ============================================================
# DATABASE FILE HELPERS
# ============================================================

def _create_database_if_missing():
    """Create local_database.json if it doesn't exist."""

    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(
                DEFAULT_DATABASE,
                file,
                indent=4,
                ensure_ascii=False
            )


def _load_database():
    """Load the complete local database."""

    _create_database_if_missing()

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return deepcopy(DEFAULT_DATABASE)

        return data

    except (json.JSONDecodeError, OSError):
        return deepcopy(DEFAULT_DATABASE)


def _save_database(data):
    """Save the complete local database."""

    temp_file = DB_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Replace old database safely.
    os.replace(temp_file, DB_FILE)


# ============================================================
# LOCAL DATABASE REFERENCE
# ============================================================

class LocalReference:
    """
    Firebase-like reference object.

    Supports:

        reference("/hotel").get()

        reference("/hotel/status").get()

        reference("/hotel/status").set(True)

        reference("/hotel/status").set("active")
    """

    def __init__(self, path):
        self.path = path.strip("/")

    def _parts(self):
        if not self.path:
            return []

        return [
            part
            for part in self.path.split("/")
            if part
        ]

    def get(self):
        """Get data from the requested path."""

        with _lock:

            data = _load_database()

            parts = self._parts()

            if not parts:
                return deepcopy(data)

            current = data

            for part in parts:

                if not isinstance(current, dict):
                    return None

                if part not in current:
                    return None

                current = current[part]

            return deepcopy(current)

    def set(self, value):
        """Set data at the requested path."""

        with _lock:

            data = _load_database()

            parts = self._parts()

            if not parts:
                data = deepcopy(value)

            else:

                current = data

                for part in parts[:-1]:

                    if part not in current:
                        current[part] = {}

                    if not isinstance(current[part], dict):
                        current[part] = {}

                    current = current[part]

                current[parts[-1]] = deepcopy(value)

            _save_database(data)

        return None


# ============================================================
# LOCAL DATABASE OBJECT
# ============================================================

class LocalDatabase:
    """
    Firebase-compatible replacement used locally.
    """

    def reference(self, path="/"):
        return LocalReference(path)


# ============================================================
# INITIALIZE LOCAL DATABASE
# ============================================================

_create_database_if_missing()

_local_db = LocalDatabase()


# ============================================================
# SAME FUNCTION NAME USED BY app.py
# ============================================================

def get_db():
    """
    Returns the local database object.

    app.py can continue using:

        db = get_db()

        db.reference("/hotel").get()

        db.reference("/hotel/crisis_active").set(True)
    """

    return _local_db