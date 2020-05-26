import os

# TODO Get these from environment
# os.environ["POSTGRES_USERNAME"] = ""
# os.environ["POSTGRES_DBNAME"] = "django-db"
# os.environ["POSTGRES_PASSWORD"] = ""
# os.environ["POSTGRES_HOST"] = "127.0.0.1"


def postgres():
    SETTINGS = {
        "username": os.environ.get("POSTGRES_USER", ""),
        "db_name": os.environ.get("POSTGRES_DB", "django-db"),
        "host": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "password": os.environ.get("POSTGRES_PASSWORD", ""),
        "port": os.environ.get("POSTGRES_PORT", 5432),
    }

    return SETTINGS


POSTGRES_CONFIG = postgres()
