from abc import ABC, abstractmethod
from typing import Dict


class ILoggingProvider(ABC):
    @abstractmethod
    def debug(self, message: str, extra_data: Dict = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str, extra_data: Dict = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str, extra_data: Dict = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str, extra_data: Dict = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def fatal(self, message: str, extra_data: Dict = None) -> None:
        raise NotImplementedError
