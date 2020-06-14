import os

POSTGRES_CONFIG = {
    "username": os.environ.get("POSTGRES_USER", "postgres"),
    "db_name": os.environ.get("POSTGRES_DB", "store"),
    "host": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
    "password": os.environ.get("POSTGRES_PASSWORD", ""),
    "port": os.environ.get("POSTGRES_PORT", 5432),
}
