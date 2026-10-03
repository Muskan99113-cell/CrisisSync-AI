import json
import os
import tempfile
import threading


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

# Vercel serverless filesystem is read-only except /tmp.
# Locally this also works without needing a project-folder DB.
DATABASE_FILE = os.path.join(
    tempfile.gettempdir(),
    "crisis_sync_database.json"
)

# RLock is important because database methods call _save_database()
# while already holding the database lock.
DATABASE_LOCK = threading.RLock()


# ============================================================
# DATABASE HELPERS
# ============================================================

def _load_database():

    if not os.path.exists(DATABASE_FILE):
        return {}

    try:

        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

            if not content:
                return {}

            data = json.loads(content)

            if isinstance(data, dict):
                return data

            return {}

    except (
        json.JSONDecodeError,
        OSError,
        TypeError
    ) as error:

        print(
            "Database read error:",
            error
        )

        return {}


def _save_database(data):

    """
    Save database atomically.

    Uses /tmp on Vercel because the deployment filesystem
    is read-only.
    """

    with DATABASE_LOCK:

        directory = os.path.dirname(
            DATABASE_FILE
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        temp_file = None

        try:

            file_descriptor, temp_file = tempfile.mkstemp(
                prefix="crisis_sync_database_",
                suffix=".tmp",
                dir=directory
            )

            with os.fdopen(
                file_descriptor,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2,
                    ensure_ascii=False
                )

                file.flush()

                try:
                    os.fsync(
                        file.fileno()
                    )
                except OSError:
                    pass

            os.replace(
                temp_file,
                DATABASE_FILE
            )

            temp_file = None

        finally:

            if (
                temp_file
                and os.path.exists(temp_file)
            ):

                try:

                    os.remove(
                        temp_file
                    )

                except OSError:

                    pass


# ============================================================
# PATH UTILITIES
# ============================================================

def _split_path(path):

    if path is None:
        return []

    path = str(path).strip()

    if not path:
        return []

    path = path.strip("/")

    if not path:
        return []

    return [
        part
        for part in path.split("/")
        if part
    ]


def _get_value(data, parts):

    current = data

    for part in parts:

        if not isinstance(
            current,
            dict
        ):
            return None

        if part not in current:
            return None

        current = current[part]

    return current


def _set_value(
    data,
    parts,
    value
):

    if not parts:
        return value

    current = data

    for part in parts[:-1]:

        if part not in current:

            current[part] = {}

        elif not isinstance(
            current[part],
            dict
        ):

            current[part] = {}

        current = current[part]

    current[parts[-1]] = value

    return data


def _delete_value(
    data,
    parts
):

    if not parts:
        return {}

    current = data

    for part in parts[:-1]:

        if not isinstance(
            current,
            dict
        ):
            return data

        if part not in current:
            return data

        current = current[part]

    if isinstance(
        current,
        dict
    ):

        current.pop(
            parts[-1],
            None
        )

    return data


# ============================================================
# DATABASE REFERENCE
# ============================================================

class LocalReference:

    def __init__(
        self,
        path=""
    ):

        self.path = (
            str(path)
            if path is not None
            else ""
        )


    # ========================================================
    # CHILD
    # ========================================================

    def child(self, key):

        if not self.path:

            new_path = str(key)

        else:

            new_path = (
                self.path.rstrip("/")
                + "/"
                + str(key).strip("/")
            )

        return LocalReference(
            new_path
        )


    # ========================================================
    # GET
    # ========================================================

    def get(self):

        with DATABASE_LOCK:

            data = _load_database()

            parts = _split_path(
                self.path
            )

            return _get_value(
                data,
                parts
            )


    # ========================================================
    # SET
    # ========================================================

    def set(self, value):

        with DATABASE_LOCK:

            data = _load_database()

            parts = _split_path(
                self.path
            )

            if not parts:

                data = value

            else:

                _set_value(
                    data,
                    parts,
                    value
                )

            _save_database(
                data
            )

            return value


    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, values):

        if not isinstance(
            values,
            dict
        ):

            raise TypeError(
                "update() requires a dictionary"
            )

        with DATABASE_LOCK:

            data = _load_database()

            parts = _split_path(
                self.path
            )

            current = _get_value(
                data,
                parts
            )

            if not isinstance(
                current,
                dict
            ):

                current = {}

            current = dict(
                current
            )

            current.update(
                values
            )

            if not parts:

                data = current

            else:

                _set_value(
                    data,
                    parts,
                    current
                )

            _save_database(
                data
            )

            return current


    # ========================================================
    # DELETE
    # ========================================================

    def delete(self):

        with DATABASE_LOCK:

            data = _load_database()

            parts = _split_path(
                self.path
            )

            data = _delete_value(
                data,
                parts
            )

            _save_database(
                data
            )


    # ========================================================
    # PUSH
    # ========================================================

    def push(self, value):

        with DATABASE_LOCK:

            data = _load_database()

            parts = _split_path(
                self.path
            )

            current = _get_value(
                data,
                parts
            )

            if not isinstance(
                current,
                dict
            ):

                current = {}

            key = (
                "item_"
                + os.urandom(6).hex()
            )

            current[key] = value

            if parts:

                _set_value(
                    data,
                    parts,
                    current
                )

            else:

                data = current

            _save_database(
                data
            )

            return LocalReference(
                self.path.rstrip("/")
                + "/"
                + key
            )


    # ========================================================
    # EXISTS
    # ========================================================

    def exists(self):

        return self.get() is not None


# ============================================================
# DATABASE OBJECT
# ============================================================

class LocalDatabase:

    def reference(
        self,
        path=""
    ):

        return LocalReference(
            path
        )


# ============================================================
# SINGLE DATABASE INSTANCE
# ============================================================

_database = LocalDatabase()


# ============================================================
# PUBLIC DATABASE FUNCTION
# ============================================================

def get_db():

    return _database