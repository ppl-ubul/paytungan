from typing import Dict
import os

from  .exceptions import BaseException

def get_db_config() -> Dict[str, str]:
    db_config = os.getenv("DB_CONFIG")
    if not db_config:
        raise BaseException("Config Key DB_CONFIG is not configured")

    db_config = db_config.split("|")
    db_config = {
        "DB_HOST": db_config[0],
        "DB_USER": db_config[1],
        "DB_PASS": db_config[2],
        "DB_NAME": db_config[3],
    }

    return db_config
