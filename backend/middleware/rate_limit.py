"""
Rate limiting middleware using Redis
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import redis
import time
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using sliding window"""

    def __init__(self, app, redis_client=None):
        super().__init__(app)
        try:
            self.redis = redis_client or redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            self.enabled = settings.RATE_LIMIT_ENABLED
        except Exception as e:
            logger.warning(f"Rate limiting disabled - Redis connection failed: {e}")
            self.enabled = False

    async def dispatch(self, request: Request, call_next: Callable):
        """Apply rate limiting"""

        if not self.enabled:
            return await call_next(request)

        # Get client identifier (IP address)
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for health checks
        if request.url.path in ["/", "/health", "/api/monitoring/health"]:
            return await call_next(request)

        # Apply stricter limits to scan endpoint
        if "/api/trends/scan" in request.url.path:
            limit = settings.RATE_LIMIT_SCAN_PER_HOUR
            window = 3600  # 1 hour
        else:
            limit = settings.RATE_LIMIT_PER_MINUTE
            window = 60  # 1 minute

        # Rate limiting key
        key = f"rate_limit:{client_ip}:{request.url.path}:{window}"

        try:
            # Increment counter
            current = self.redis.incr(key)

            # Set expiry on first request
            if current == 1:
                self.redis.expire(key, window)

            # Check if limit exceeded
            if current > limit:
                logger.warning(
                    f"Rate limit exceeded for {client_ip} on {request.url.path}: "
                    f"{current}/{limit} in {window}s window"
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Max {limit} requests per {window} seconds.",
                    headers={"Retry-After": str(window)}
                )

            # Add rate limit headers to response
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(limit)
            response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current))
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + window)

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Rate limiting error: {e}", exc_info=True)
            # On error, allow request through
            return await call_next(request)


def rate_limit_dependency():
    """Dependency for manual rate limit checking"""
    # Can be used for additional endpoint-specific rate limiting
    pass
