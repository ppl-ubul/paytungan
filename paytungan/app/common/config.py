from typing import Dict
import os


def get_db_config() -> Dict[str, str]:
    db_config = os.getenv("DB_CONFIG")
    db_config = db_config.split("|")
    db_config = {
        "DB_HOST": db_config[0],
        "DB_USER": db_config[1],
        "DB_PASS": db_config[2],
        "DB_NAME": db_config[3],
    }

    return db_config
