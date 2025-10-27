"""
Request logging middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing information"""

    async def dispatch(self, request: Request, call_next: Callable):
        """Log request and response"""
        start_time = time.time()

        # Generate request ID
        request_id = f"{int(start_time * 1000)}-{id(request)}"
        request.state.request_id = request_id

        # Log request
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            logger.info(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Duration: {process_time:.3f}s"
            )

            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"

            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"Error: {str(e)} - "
                f"Duration: {process_time:.3f}s",
                exc_info=True
            )
            raise
