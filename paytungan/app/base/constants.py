from enum import Enum
import os


DEFAULT_LOGGER = "paytungan-backend"
CURRENT_ENV = os.getenv("APP_ENV", "local")
SERVICE_ACCOUNT_FILE = (
    "firebase-admin-secret.json" if CURRENT_ENV == "local" else "firebase-admin.json"
)
FIREBASE_PROJECT_ID = "paytungan"

DB_CONFIG = "DB_CONFIG"
FIREBASE_PRIVATE_KEY_ID = "FIREBASE_PRIVATE_KEY_ID"
FIREBASE_PRIVATE_KEY = "FIREBASE_PRIVATE_KEY"


class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    TEST = "test"