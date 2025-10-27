"""
Global error handling middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handler for consistent error responses"""

    async def dispatch(self, request: Request, call_next: Callable):
        """Handle errors consistently"""
        try:
            return await call_next(request)
        except ValidationError as e:
            logger.warning(f"Validation error on {request.url.path}: {e}")
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "success": False,
                    "error": "Validation Error",
                    "detail": str(e),
                    "error_code": "VALIDATION_ERROR"
                }
            )
        except SQLAlchemyError as e:
            logger.error(f"Database error on {request.url.path}: {e}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": "Database Error",
                    "detail": "An error occurred while processing your request",
                    "error_code": "DATABASE_ERROR"
                }
            )
        except Exception as e:
            logger.error(
                f"Unhandled error on {request.url.path}: {e}",
                exc_info=True
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": "Internal Server Error",
                    "detail": str(e) if logger.level == logging.DEBUG else "An unexpected error occurred",
                    "error_code": "INTERNAL_ERROR"
                }
            )
