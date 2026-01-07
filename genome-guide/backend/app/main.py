"""
    Main entry point for the FastAPI application.
    Configures the FastAPI app, including middleware, routing, and exception handlers.
    Initializes logging and ensures database tables are created on startup.
    """
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .api.api_v1 import api_router
from .core.logging_config import setup_logging
from .db.session import Base, get_engine # Import Base and get_engine
from .config import get_settings # Import get_settings
from http import HTTPStatus # Import HTTPStatus

def create_app() -> FastAPI:
    # Call setup_logging at the very beginning to configure logging before any other module imports
    setup_logging()
    logger = logging.getLogger(__name__)

    app = FastAPI(
        title="Genome Guides API",
        description="An API for browsing and searching human genome data.",
        version="0.1.0",
    )

    # Log application startup
    logger.info("Genome Guides API application starting up.")

    # --- CORS MIDDLEWARE ---
    _settings = get_settings() # Get settings object
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.CORS_ORIGINS, # Use settings from get_settings()
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # -----------------------------------------

    @app.on_event("startup")
    def on_startup():
        logger.info("Application starting up...")
        # Ensure tables are created if they don't exist
        # This is useful for development and testing, Alembic handles migrations in production
        Base.metadata.create_all(bind=get_engine()) # Use get_engine()

    # --- EXCEPTION HANDLERS ---
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handles HTTPException to return a consistent JSON error response.
        """
        logger.warning(
            f"HTTPException: {exc.status_code} - {exc.detail} for URL: {request.url}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handles all other unhandled exceptions, returning a 500 Internal Server Error.
        """
        # Log the full traceback for unhandled exceptions
        logger.exception(f"Unhandled exception for URL: {request.url}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."},
        )
    # -----------------------------------------


    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Genome Guides API!"}

    app.include_router(api_router, prefix="/api/v1")
    return app

app = create_app()