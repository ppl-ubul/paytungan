from typing import Dict
import os

from paytungan.app.base.constants import (
    DB_CONFIG,
    FIREBASE_PRIVATE_KEY,
    FIREBASE_PRIVATE_KEY_ID,
)

from .exceptions import BaseException


def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise BaseException(f"Config Key {key} is not configured")

    return value


def get_db_config() -> Dict[str, str]:
    db_config = get_env(DB_CONFIG)

    db_config = db_config.split("|")
    db_config = {
        "DB_HOST": db_config[0],
        "DB_USER": db_config[1],
        "DB_PASS": db_config[2],
        "DB_NAME": db_config[3],
    }

    return db_config


def get_firebase_config() -> Dict[str, str]:
    return {
        "type": "service_account",
        "project_id": "paytungan",
        "private_key_id": get_env(FIREBASE_PRIVATE_KEY_ID),
        "private_key": get_env(FIREBASE_PRIVATE_KEY).replace("\\n", "\n"),
        "client_email": "firebase-adminsdk-4v672@paytungan.iam.gserviceaccount.com",
        "client_id": "113476718206995380065",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4v672%40paytungan.iam.gserviceaccount.com",
    }
