from enum import Enum


DEFAULT_LOGGER = "paytungan-backend"


class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
