import os

# TODO Get these from environment
# os.environ["POSTGRES_USERNAME"] = ""
# os.environ["POSTGRES_DBNAME"] = "django-db"
# os.environ["POSTGRES_PASSWORD"] = ""
# os.environ["POSTGRES_HOST"] = "127.0.0.1"


def postgres():

    DEFAULTS = {
        "username": "",
        "db_name": "django-db",
        "password": "",
        "host": "127.0.0.1",
        "port": 5432,
    }

    SETTINGS = {
        "username": os.environ.get("POSTGRES_USER", DEFAULTS["username"]),
        "db_name": os.environ.get("POSTGRES_DB", DEFAULTS["password"]),
        "host": os.environ.get("POSTGRES_HOST", DEFAULTS["host"]),
        "password": os.environ.get("POSTGRES_PASSWORD", DEFAULTS["password"]),
        "port": os.environ.get("POSTGRES_PORT", 5432),
    }

    return {
        k: v_default if k not in SETTINGS or SETTINGS[k] is None else SETTINGS[k]
        for k, v_default in DEFAULTS.items()
    }


POSTGRES_CONFIG = postgres()
