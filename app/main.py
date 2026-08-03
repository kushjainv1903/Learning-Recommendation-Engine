"""FastAPI application entry point for LearnPath AI."""

import logging
from collections.abc import Callable

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import router
from app.config import (
    API_DESCRIPTION,
    API_TITLE,
    API_VERSION,
    BODY_HTTP_METHODS,
    INVALID_JSON_ERROR,
    JSON_CONTENT_TYPES,
    MAX_REQUEST_SIZE_BYTES,
    METHOD_NOT_ALLOWED_ERROR,
    PAYLOAD_TOO_LARGE_ERROR,
    UNKNOWN_ERROR,
    UNSUPPORTED_MEDIA_TYPE_ERROR,
    VALIDATION_ERROR,
    validate_config,
)
from app.core.exceptions import ConfigurationException
from app.utils.logger import configure_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.

    Raises:
        ConfigurationException: If startup configuration is invalid.

    Example:
        >>> application = create_app()
        >>> application.title
        'Learning Recommendation API'
    """
    configure_logging()
    validate_config()

    application = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )
    application.include_router(router)
    _register_exception_handlers(application)
    _register_middleware(application)

    logger.info("FastAPI application configured")
    return application


def _register_exception_handlers(application: FastAPI) -> None:
    """Register application-level exception handlers.

    Args:
        application: FastAPI app that receives exception handlers.

    Returns:
        None.

    Raises:
        None.

    Example:
        >>> app_instance = FastAPI()
        >>> _register_exception_handlers(app_instance)
    """

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning("Validation failed for request path %s", request.url.path)
        if _is_json_decode_error(exc):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": INVALID_JSON_ERROR},
            )
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": VALIDATION_ERROR,
                "details": _format_validation_errors(exc),
            },
        )

    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        logger.warning(
            "HTTP error for request path %s: %s",
            request.url.path,
            exc.status_code,
        )
        if exc.status_code == 405:
            return JSONResponse(
                status_code=405,
                content={"success": False, "error": METHOD_NOT_ALLOWED_ERROR},
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": str(exc.detail)},
        )

    @application.exception_handler(ConfigurationException)
    async def configuration_exception_handler(
        request: Request, exc: ConfigurationException
    ) -> JSONResponse:
        logger.critical("Configuration error for request path %s", request.url.path)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": UNKNOWN_ERROR},
        )

    @application.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            "Unexpected error for request path %s",
            request.url.path,
            exc_info=exc,
        )
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": UNKNOWN_ERROR},
        )


def _register_middleware(application: FastAPI) -> None:
    """Register application middleware.

    Args:
        application: FastAPI app that receives middleware.

    Returns:
        None.

    Raises:
        None.

    Example:
        >>> app_instance = FastAPI()
        >>> _register_middleware(app_instance)
    """

    @application.middleware("http")
    async def log_requests(
        request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        logger.info("API request received: %s %s", request.method, request.url.path)
        validation_response = _validate_request_boundary(request)
        if validation_response is not None:
            logger.warning(
                "Request boundary validation failed: %s %s",
                request.method,
                request.url.path,
            )
            return validation_response

        response = await call_next(request)
        logger.info(
            "API request completed: %s %s %s",
            request.method,
            request.url.path,
            response.status_code,
        )
        return response


def _validate_request_boundary(request: Request) -> JSONResponse | None:
    """Validate transport-level request requirements.

    Args:
        request: Incoming FastAPI request.

    Returns:
        JSON error response when validation fails, otherwise None.

    Raises:
        None.

    Example:
        >>> isinstance(_validate_request_boundary, object)
        True
    """
    size_response = _validate_request_size(request)
    if size_response is not None:
        return size_response
    return _validate_content_type(request)


def _validate_request_size(request: Request) -> JSONResponse | None:
    """Validate maximum request size from Content-Length.

    Args:
        request: Incoming FastAPI request.

    Returns:
        JSON error response when the payload is too large, otherwise None.

    Raises:
        None.

    Example:
        >>> isinstance(_validate_request_size, object)
        True
    """
    content_length = request.headers.get("content-length")
    if content_length is None:
        return None
    try:
        request_size = int(content_length)
    except ValueError:
        return None
    if request_size <= MAX_REQUEST_SIZE_BYTES:
        return None
    return JSONResponse(
        status_code=413,
        content={"success": False, "error": PAYLOAD_TOO_LARGE_ERROR},
    )


def _validate_content_type(request: Request) -> JSONResponse | None:
    """Validate JSON content type for body-bearing methods.

    Args:
        request: Incoming FastAPI request.

    Returns:
        JSON error response when content type is unsupported, otherwise None.

    Raises:
        None.

    Example:
        >>> isinstance(_validate_content_type, object)
        True
    """
    if request.method not in BODY_HTTP_METHODS:
        return None
    content_length = request.headers.get("content-length")
    if content_length == "0":
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": INVALID_JSON_ERROR},
        )
    content_type = request.headers.get("content-type")
    if content_type is None:
        return None
    normalized_type = content_type.split(";", maxsplit=1)[0].strip().lower()
    if normalized_type in JSON_CONTENT_TYPES:
        return None
    return JSONResponse(
        status_code=415,
        content={"success": False, "error": UNSUPPORTED_MEDIA_TYPE_ERROR},
    )


def _is_json_decode_error(exc: RequestValidationError) -> bool:
    """Detect malformed JSON validation failures.

    Args:
        exc: FastAPI request validation exception.

    Returns:
        True when validation failed because JSON could not be decoded.

    Raises:
        None.

    Example:
        >>> isinstance(_is_json_decode_error, object)
        True
    """
    return any(error.get("type") == "json_invalid" for error in exc.errors())


def _format_validation_errors(exc: RequestValidationError) -> list[dict[str, str]]:
    """Format validation errors for the documented API contract.

    Args:
        exc: FastAPI request validation exception.

    Returns:
        List of field/message dictionaries.

    Raises:
        None.

    Example:
        >>> isinstance(_format_validation_errors, object)
        True
    """
    return [
        {
            "field": _format_error_field(error.get("loc", ())),
            "message": _format_error_message(str(error.get("msg", ""))),
        }
        for error in exc.errors()
    ]


def _format_error_field(location: object) -> str:
    if not isinstance(location, tuple):
        return str(location)
    parts = [str(part) for part in location if part != "body"]
    return ".".join(parts)


def _format_error_message(message: str) -> str:
    if message.startswith("Value error, "):
        message = message.removeprefix("Value error, ")
    return message


app = create_app()
