import uuid
import threading
import logging
import time
from json_log_formatter import JSONFormatter

from ..base.constants import DEFAULT_LOGGER

local = threading.local()
REQUEST_HEADER = "x-request-id"
logger = logging.getLogger(DEFAULT_LOGGER)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)

        # Code to be executed for each request/response after
        # the view is called.
        response = self.process_response(request, self.get_response(request))

        return response

    def process_request(self, request):
        request_id = self._get_request_id(request)
        local.request_id = request_id
        local.request_path = request.path
        local.request_payload = self._get_request_payload(request)
        request.id = request_id

    def get_log_message(self, request, response):
        message = "%s %s %s" % (request.method, request.path, response.status_code)
        return message

    def process_response(self, request, response):
        response[REQUEST_HEADER] = request.id

        # Only log /api
        if "/api" not in request.path:
            return response

        logger.info(self.get_log_message(request, response))

        try:
            del local.request_id
            del local.request_path
        except AttributeError:
            pass

        return response

    def _get_request_id(self, request) -> str:
        return request.headers.get(REQUEST_HEADER, self._generate_id())

    def _generate_id(self) -> str:
        return uuid.uuid4().hex

    def _get_request_payload(self, request):
        if request.method == "GET":
            return request.GET
        else:
            return request.body

    @staticmethod
    def get_request_id() -> str:
        return local.request_id


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.request_id = getattr(local, "request_id", "default")
        record.request_path = getattr(local, "request_path", "default")
        record.request_payload = getattr(local, "request_payload", "default")
        return True


class JSONFormatter(JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra["name"] = record.name
        extra["level"] = record.levelname
        extra["request_id"] = record.request_id
        extra["request_path"] = record.request_path
        extra["request_payload"] = record.request_payload
        extra["time"] = time.strftime(
            "%Y-%m-%d %H:%M:%S%z", time.localtime(record.created)
        )
        extra["epoch_time"] = record.created
        extra["at"] = f"{record.module}.{record.funcName}:{record.lineno}"
        extra["message"] = message

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
