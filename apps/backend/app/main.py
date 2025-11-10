from fastapi import FastAPI
from app.core.config import settings
from app.api import auth_controller, user_controller
from app.core.database import Base, engine
from app.domain import user_model, project_model, tagging_model # Import models to ensure they are registered with Base
import logging
from fastapi.exceptions import HTTPException
from app.core.exception_handlers import http_exception_handler, generic_exception_handler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables():
    """Creates database tables based on SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)

def get_application() -> FastAPI:
    # Initialize FastAPI application
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
    )

    # Include routers
    application.include_router(auth_controller.router, prefix=settings.API_PREFIX)
    application.include_router(user_controller.router, prefix=settings.API_PREFIX)

    # NOTE: Add middleware for observability/audit logging (Story 1.4) here later.

    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)

    return application

# Create tables on startup (for local development/testing)
create_tables()

app = get_application()