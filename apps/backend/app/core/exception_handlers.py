import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

logger = logging.getLogger(__name__)

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail} for URL: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled Exception: {exc} for URL: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred."},
    )