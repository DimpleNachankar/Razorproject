"""
Middleware for TRUSTSHIELD API
CORS, logging, error handling, and request tracking
"""

import time
import uuid
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging

from app.config import get_settings, LogMessages, ErrorCodes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("trustshield")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging all requests and responses
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        
        settings = get_settings()
        if settings.VERBOSE_LOGGING:
            logger.info(LogMessages.REQUEST_RECEIVED.format(
                method=request.method,
                path=request.url.path
            ))
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log completion
            if settings.VERBOSE_LOGGING:
                logger.info(LogMessages.REQUEST_COMPLETED.format(
                    method=request.method,
                    path=request.url.path,
                    status_code=response.status_code,
                    duration=f"{duration_ms:.2f}"
                ))
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Processing-Time-MS"] = f"{duration_ms:.2f}"
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(LogMessages.ERROR_OCCURRED.format(
                error_type=type(e).__name__,
                message=str(e)
            ))
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": ErrorCodes.INTERNAL_ERROR,
                    "message": "Internal server error occurred",
                    "request_id": request_id
                },
                headers={
                    "X-Request-ID": request_id,
                    "X-Processing-Time-MS": f"{duration_ms:.2f}"
                }
            )


class DemoModeMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject demo mode headers
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        settings = get_settings()
        if settings.DEMO_MODE:
            response.headers["X-Demo-Mode"] = "true"
            response.headers["X-Demo-Message"] = "Using mock data - no real payment processing"
        
        return response


def setup_cors(app):
    """
    Configure CORS middleware
    
    Args:
        app: FastAPI application instance
    """
    settings = get_settings()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
        expose_headers=[
            "X-Request-ID",
            "X-Processing-Time-MS",
            "X-Demo-Mode",
            "X-Demo-Message"
        ]
    )
    
    logger.info(f"CORS configured with allowed origins: {settings.allowed_origins_list}")


def setup_middleware(app):
    """
    Configure all middleware
    
    Args:
        app: FastAPI application instance
    """
    
    # Add CORS first (outermost middleware)
    setup_cors(app)
    
    # Add custom middleware
    app.add_middleware(DemoModeMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    
    logger.info("Middleware configured successfully")


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

async def validation_exception_handler(request: Request, exc):
    """
    Handle Pydantic validation errors
    """
    from fastapi.exceptions import RequestValidationError
    
    logger.warning(f"Validation error: {exc}")
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "error_code": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": ErrorCodes.VALIDATION_ERROR,
            "message": "Invalid request parameters",
            "details": errors,
            "request_id": getattr(request.state, "request_id", None)
        }
    )


async def http_exception_handler(request: Request, exc):
    """
    Handle HTTP exceptions
    """
    from fastapi import HTTPException
    
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    # If detail is already a dict (from our API routes), return it
    if isinstance(exc.detail, dict):
        content = exc.detail
        if "request_id" not in content:
            content["request_id"] = getattr(request.state, "request_id", None)
    else:
        content = {
            "error": "HTTP_ERROR",
            "message": str(exc.detail),
            "request_id": getattr(request.state, "request_id", None)
        }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all other exceptions
    """
    logger.error(f"Unhandled exception: {type(exc).__name__} - {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": ErrorCodes.INTERNAL_ERROR,
            "message": "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", None)
        }
    )


def setup_exception_handlers(app):
    """
    Configure exception handlers
    
    Args:
        app: FastAPI application instance
    """
    from fastapi.exceptions import RequestValidationError
    from fastapi import HTTPException
    
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("Exception handlers configured successfully")


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "setup_middleware",
    "setup_cors",
    "setup_exception_handlers",
    "RequestLoggingMiddleware",
    "DemoModeMiddleware"
]
