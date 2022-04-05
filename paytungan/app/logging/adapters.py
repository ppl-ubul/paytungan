import logging
from typing import Dict

from sentry_sdk import capture_message

from paytungan.app.common.utils import DictionaryUtil
from .interface import ILoggingProvider
from paytungan.app.base.constants import DEFAULT_LOGGER


class LoggingProvider(ILoggingProvider):
    def __init__(self):
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def debug(self, message: str, extra_data: Dict = None) -> None:
        if not extra_data:
            extra_data = {}

        self.logger.debug(
            message,
            extra={
                "extra": DictionaryUtil.transform_into_jsonable_dictionary(extra_data),
            },
        )

    def info(self, message: str, extra_data: Dict = None) -> None:
        if not extra_data:
            extra_data = {}

        self.logger.info(
            message,
            extra={
                "extra": DictionaryUtil.transform_into_jsonable_dictionary(extra_data),
            },
        )

    def warning(self, message: str, extra_data: Dict = None) -> None:
        if not extra_data:
            extra_data = {}

        self.logger.warning(
            message,
            extra={
                "extra": DictionaryUtil.transform_into_jsonable_dictionary(extra_data),
            },
        )

        capture_message(message, level="warning", extras=extra_data)

    def error(self, message: str, extra_data: Dict = None) -> None:
        if not extra_data:
            extra_data = {}

        self.logger.error(
            message,
            extra={
                "extra": DictionaryUtil.transform_into_jsonable_dictionary(extra_data),
            },
        )

        capture_message(message, level="error", extras=extra_data)

    def fatal(self, message: str, extra_data: Dict = None) -> None:
        if not extra_data:
            extra_data = {}

        self.logger.fatal(
            message,
            extra={
                "extra": DictionaryUtil.transform_into_jsonable_dictionary(extra_data),
            },
        )

        capture_message(message, level="fatal", extras=extra_data)
