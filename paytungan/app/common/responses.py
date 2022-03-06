from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

ValidationErrorType = Dict[str, List[str]]
ResponseJson = Dict[str, any]


@dataclass
class ErrorDetail:
    error_message: str
    code: Optional[int]
    validation_error: ValidationErrorType = field(default_factory=list)


@dataclass(init=False)
class ErrorResponse:
    errors: ErrorDetail

    def __init__(
        self,
        error_message: str = "",
        validation_error: ValidationErrorType = None,
        code: int = None,
    ):
        validation_error = validation_error or {}
        self.errors = ErrorDetail(
            error_message=error_message, validation_error=validation_error, code=code
        )

    @property
    def error(self) -> ResponseJson:
        return asdict(self)
