from fastapi import FastAPI
from app.core.config import settings
from app.api import auth_controller, user_controller
from app.core.database import Base, engine
from app.domain import user_model, project_model, tagging_model # Import models to ensure they are registered with Base
import logging
from fastapi.exceptions import HTTPException
from sqlalchemy import DDL, event
from pydantic import ValidationError
from app.core.exceptions import APIException
from app.core.exception_handlers import (
    http_exception_handler,
    generic_exception_handler,
    api_exception_handler,
    validation_exception_handler
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_drop_cascade_for_postgres():
    """Registers DDL event listeners to append CASCADE to DROP TABLE IF EXISTS statements for PostgreSQL."""
    if engine.dialect.name == 'postgresql':
        for table in Base.metadata.tables.values():
            event.listen(
                table,
                "before_drop",
                DDL("DROP TABLE IF EXISTS %(table)s CASCADE")
            )

register_drop_cascade_for_postgres()

def create_tables(drop_first: bool = False):
    """Creates database tables based on SQLAlchemy models."""
    if drop_first:
        logger.warning("Dropping all existing database tables...")
        # We rely on the DDL event listener to handle CASCADE and IF EXISTS
        Base.metadata.drop_all(bind=engine)
        logger.warning("Finished dropping tables.")
        
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Finished creating tables.")

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

    application.add_exception_handler(APIException, api_exception_handler)
    application.add_exception_handler(ValidationError, validation_exception_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(Exception, generic_exception_handler)

    return application

# Create tables on startup (for local development/testing)
create_tables(drop_first=True) # Force recreation of tables during development

app = get_application()