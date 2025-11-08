from fastapi import FastAPI
from app.core.config import settings
from app.api import auth_controller, user_controller
from app.core.database import Base, engine
from app.domain import user_model # Import models to ensure they are registered with Base

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

    return application

# Create tables on startup (for local development/testing)
create_tables()

app = get_application()