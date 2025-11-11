from typing import Dict, Any

# Standardized Message Keys for API Responses
# These keys are used internally for logging and externalized in error responses.

class MessageKeys:
    # Success Messages
    USER_REGISTERED_SUCCESS = "USER_REGISTERED_SUCCESS"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    TOKEN_REFRESH_SUCCESS = "TOKEN_REFRESH_SUCCESS"
    PROFILE_RETRIEVED_SUCCESS = "PROFILE_RETRIEVED_SUCCESS"
    PROFILE_UPDATED_SUCCESS = "PROFILE_UPDATED_SUCCESS"

    # Error Messages (API Exceptions)
    EMAIL_ALREADY_REGISTERED = "EMAIL_ALREADY_REGISTERED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    FORBIDDEN_ACCESS = "FORBIDDEN_ACCESS"
    BAD_REQUEST = "BAD_REQUEST"

    # System/Unhandled Errors
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    DATABASE_PROGRAMMING_ERROR = "DATABASE_PROGRAMMING_ERROR"


MESSAGE_MAP: Dict[str, Dict[str, Any]] = {
    # Successes
    MessageKeys.USER_REGISTERED_SUCCESS: {"message": "User registered successfully."},
    MessageKeys.LOGIN_SUCCESS: {"message": "Login successful."},
    MessageKeys.TOKEN_REFRESH_SUCCESS: {"message": "Token refresh successful."},
    MessageKeys.PROFILE_RETRIEVED_SUCCESS: {"message": "User profile retrieved successfully."},
    MessageKeys.PROFILE_UPDATED_SUCCESS: {"message": "User profile updated successfully."},

    # Errors
    MessageKeys.EMAIL_ALREADY_REGISTERED: {"message": "Email already registered."},
    MessageKeys.INVALID_CREDENTIALS: {"message": "Invalid credentials."},
    MessageKeys.INVALID_TOKEN: {"message": "Invalid token or token expired."},
    MessageKeys.USER_NOT_FOUND: {"message": "User not found."},
    MessageKeys.FORBIDDEN_ACCESS: {"message": "Permission denied."},
    MessageKeys.BAD_REQUEST: {"message": "Bad request."},

    # System Errors
    MessageKeys.UNEXPECTED_ERROR: {"message": "An unexpected error occurred."},
    MessageKeys.VALIDATION_FAILED: {"message": "Validation failed."},
    MessageKeys.DATABASE_PROGRAMMING_ERROR: {"message": "A database error occurred. Please contact support with the correlation ID."},
}

def get_message(key: str) -> str:
    """Retrieves the human-readable message for a given key."""
    return MESSAGE_MAP.get(key, {}).get("message", "Unknown message key.")