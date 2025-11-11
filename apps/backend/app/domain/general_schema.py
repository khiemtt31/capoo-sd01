from typing import Any, Generic, Optional, TypeVar, List, Dict
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')

class PaginationMetadata(BaseModel):
    """Metadata for pagination."""
    page: int = Field(..., description="Current page number (1-based)")
    per_page: int = Field(..., description="Number of items per page")
    total_items: int = Field(..., description="Total number of items across all pages")
    total_pages: int = Field(..., description="Total number of pages")

class GeneralResponse(GenericModel, Generic[T]):
    """Standardized API response structure."""
    status: str = Field(..., description="Status of the request (e.g., 'success', 'error')")
    message: str = Field(..., description="A human-readable message describing the response")
    data: Optional[T] = Field(None, description="The main response data payload")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata (e.g., pagination)")

    class Config:
        arbitrary_types_allowed = True

# Specific response types for convenience
class SuccessResponse(GeneralResponse[T]):
    status: str = "success"

class ErrorResponse(GeneralResponse[T]):
    status: str = "error"
    data: Optional[T] = None # Ensure data is None for error responses