import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.core.exceptions import APIException
from app.domain.general_schema import ErrorResponse
from app.core.messages import MessageKeys, get_message

logger = logging.getLogger(__name__)

async def api_exception_handler(request: Request, exc: APIException):
    """Handles custom API exceptions."""
    logger.warning(f"API Exception: {exc.status_code} - {exc.detail} for URL: {request.url}")
    
    # Determine the human-readable message. If exc.detail is a known key, use the mapped message.
    # Otherwise, treat it as a custom detail string.
    message_key = exc.detail if isinstance(exc.detail, str) else MessageKeys.UNEXPECTED_ERROR
    
    response_content = ErrorResponse(
        message=get_message(message_key),
        status="error",
        data=None,
        metadata={"error_type": exc.__class__.__name__, "message_key": message_key}
    ).dict()

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
        headers=exc.headers
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles standard FastAPI HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail} for URL: {request.url}")
    
    response_content = ErrorResponse(
        message=str(exc.detail),
        status="error",
        data=None,
        metadata={"error_type": "HTTPException"}
    ).dict()

    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
        headers=getattr(exc, "headers", None)
    )

async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handles Pydantic validation errors."""
    logger.error(f"Validation Error: {exc} for URL: {request.url}")
    
    error_details = exc.errors()
    
    response_content = ErrorResponse(
        message="Validation failed",
        status="error",
        data={"details": error_details},
        metadata={"error_type": "ValidationError"}
    ).dict()

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_content,
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handles all other unhandled exceptions."""
    logger.exception(f"Unhandled Exception: {exc} for URL: {request.url}")
    
    response_content = ErrorResponse(
        message=get_message(MessageKeys.UNEXPECTED_ERROR),
        status="error",
        data=None,
        metadata={"error_type": exc.__class__.__name__}
    ).dict()

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_content,
    )