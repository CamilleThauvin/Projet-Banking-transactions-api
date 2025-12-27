"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from banking_api.core.config import settings
from banking_api.routes import customers, fraud, stats, system, transactions
from banking_api.services.data_loader import load_transactions_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Loads transaction data on startup.
    """
    # Startup
    logger.info("Starting Banking Transactions API...")
    try:
        load_transactions_data()
        logger.info("Transaction data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load transaction data: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Banking Transactions API...")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router)
app.include_router(stats.router)
app.include_router(fraud.router)
app.include_router(customers.router)
app.include_router(system.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Banking Transactions API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }

