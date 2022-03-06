from enum import Enum


DEFAULT_LOGGER = "paytungan-backend"
SERVICE_ACCOUNT_FILE = "./firebase-admin-secret.json"
FIREBASE_PROJECT_ID = "paytungan"


class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    TEST = "test"
