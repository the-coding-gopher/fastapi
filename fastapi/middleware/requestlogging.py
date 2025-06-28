import logging
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        logger_name: str = "fastapi.requests",
        log_level: int = logging.INFO,
        enabled: bool = True,
    ):
        super().__init__(app)
        self.logger = logging.getLogger(logger_name)
        self.log_level = log_level
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.enabled:
            return await call_next(request)
            
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        
        self.logger.log(
            self.log_level,
            f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s"
        )
        
        return response


def add_request_logging_middleware(
    app,
    settings=None,
    **kwargs
):
    """
    Add request duration logging middleware to a FastAPI app.
    
    Args:
        app: FastAPI application instance
        settings: RequestLoggingSettings instance, or None to use defaults
        **kwargs: Override specific settings
    """
    if settings is None:
        from .settings import RequestLoggingSettings
        settings = RequestLoggingSettings(**kwargs)
    
    app.add_middleware(
        RequestLoggingMiddleware,
        logger_name=settings.request_logging_logger_name,
        log_level=settings.request_logging_level,
        enabled=settings.request_logging_enabled,
    )
