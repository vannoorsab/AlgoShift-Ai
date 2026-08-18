from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger

class TechScrollBaseException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class EntityNotFoundException(TechScrollBaseException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class DatabaseException(TechScrollBaseException):
    def __init__(self, message: str):
        super().__init__(
            message=f"Database operation error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class ValidationException(TechScrollBaseException):
    def __init__(self, message: str, details: dict = None):
        # Use HTTP_422_UNPROCESSABLE_CONTENT directly to avoid Starlette deprecation warning
        status_code_val = getattr(status, 'HTTP_422_UNPROCESSABLE_CONTENT', 422)
        super().__init__(
            message=message,
            status_code=status_code_val,
            details=details
        )

async def techscroll_exception_handler(request: Request, exc: TechScrollBaseException):
    logger.error(f"Error handling request {request.method} {request.url}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception during request {request.method} {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred on the server.",
            "details": str(exc) if request.app.debug else {}
        }
    )
