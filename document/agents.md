# Agent Context Reading Guide

This guide outlines the recommended approach for reading project documentation and source code to quickly establish context and implement new features or fixes.

## 1. Project Structure Overview

Start by reviewing the file structure to understand the separation of concerns:

*   **`apps/backend/`**: Contains the Python/FastAPI application.
    *   **`app/core/`**: Core utilities, configuration, security, and global exception handling (`exceptions.py`, `exception_handlers.py`).
    *   **`app/domain/`**: Pydantic schemas (data transfer objects, response models like `general_schema.py`) and SQLAlchemy models.
    *   **`app/data/`**: Repository layer (data access logic).
    *   **`app/services/`**: Business logic layer. This is where core functionality resides and custom exceptions are raised.
    *   **`app/api/`**: FastAPI controllers (API endpoints).
*   **`apps/frontend/`**: Contains the Next.js application.
*   **`packages/shared/`**: Contains shared TypeScript schemas/types used across the monorepo.
*   **`document/`**: Contains all project documentation.

## 2. Key Documentation Files

Prioritize reading these documents for architectural and implementation context:

| Document Path | Purpose |
| :--- | :--- |
| `document/architecture/project-context-organization.md` | High-level project organization and context. |
| `document/implementation/backend_conventions.md` | Detailed conventions for backend development, including API design, response standardization, and error handling. **(Crucial for coding)** |
| `document/implementation/backend_layered_structure.md` | Explains the separation of Repository, Service, and Controller layers. |
| `document/business-logic/business_logic_overview.md` | Overview of the application's business domain. |
| `document/sprints/sprint-*-detailed-breakdown.md` | Specific implementation details and goals for current/past sprints. |

## 3. Understanding API Implementation Flow

When implementing or debugging an API endpoint, follow this flow:

1.  **Controller (`app/api/*_controller.py`):**
    *   Check the route definition, dependencies (`Depends`), request body schema (Pydantic DTOs), and the expected `response_model` (should be `GeneralResponse[...]`).
    *   Note the explicit error responses defined using the `responses` parameter.
2.  **Service (`app/services/*_service.py`):**
    *   Review the business logic implementation.
    *   Identify where data validation or business rules are enforced.
    *   **Crucially, observe which custom exceptions (`app.core.exceptions`) are raised** (e.g., `ConflictException`, `UnauthorizedException`).
3.  **Repository (`app/data/*_repository.py`):**
    *   Understand how data is retrieved, created, or updated in the database.
4.  **Error Handling:**
    *   Remember that custom exceptions raised in the Service layer are automatically caught by the global handlers in `app/core/exception_handlers.py` and formatted into the standardized `ErrorResponse` structure defined in `app/domain/general_schema.py`.

## 4. Schema Reference

*   **Successful Responses:** Always conform to `GeneralResponse` / `SuccessResponse` (`app/domain/general_schema.py`).
*   **Error Responses:** Always conform to `ErrorResponse` (`app/domain/general_schema.py`).
*   **Data Models:** Refer to `app/domain/*_schema.py` for Pydantic schemas and `app/domain/*_model.py` for SQLAlchemy models.