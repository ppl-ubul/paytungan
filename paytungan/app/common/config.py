from typing import Dict
import os

from .exceptions import BaseException


def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise BaseException(f"Config Key {key} is not configured")

    return value


def get_db_config() -> Dict[str, str]:
    db_config = get_env("DB_CONFIG")

    db_config = db_config.split("|")
    db_config = {
        "DB_HOST": db_config[0],
        "DB_USER": db_config[1],
        "DB_PASS": db_config[2],
        "DB_NAME": db_config[3],
    }

    return db_config
