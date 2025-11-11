from typing import Any, Dict, Optional
from app.core.messages import MessageKeys, get_message

class APIException(Exception):
    """Base class for all API exceptions."""
    status_code: int = 500
    detail: Any = MessageKeys.UNEXPECTED_ERROR
    headers: Optional[Dict[str, Any]] = None

    def __init__(self, detail: Any = None, status_code: Optional[int] = None, headers: Optional[Dict[str, Any]] = None, message_key: Optional[str] = None):
        if message_key is not None:
            self.detail = message_key
        elif detail is not None:
            self.detail = detail
        
        if status_code is not None:
            self.status_code = status_code
        if headers is not None:
            self.headers = headers
        
        # The exception message itself will be the key or custom detail
        super().__init__(self.detail)

class NotFoundException(APIException):
    status_code = 404
    detail = MessageKeys.USER_NOT_FOUND # Default to user not found, can be overridden

class ConflictException(APIException):
    status_code = 409
    detail = MessageKeys.EMAIL_ALREADY_REGISTERED # Default to registration conflict

class UnauthorizedException(APIException):
    status_code = 401
    detail = MessageKeys.INVALID_CREDENTIALS # Default to invalid credentials
    
class ForbiddenException(APIException):
    status_code = 403
    detail = MessageKeys.FORBIDDEN_ACCESS

class BadRequestException(APIException):
    status_code = 400
    detail = MessageKeys.BAD_REQUEST