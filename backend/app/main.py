"""FastAPI application entry point.

Wires middleware, CORS, exception handlers, and routers.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import customers, dashboard, orders, products
from app.core.config import settings
from app.exceptions import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description=(
        "REST API for managing products, customers and orders with inventory tracking."
    ),
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS - allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized exception handlers
register_exception_handlers(app)


# Register routers
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(customers.router, prefix=settings.API_V1_PREFIX)
app.include_router(orders.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
def root() -> dict:
    """Health-check root."""
    return {
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health() -> dict:
    """Health check."""
    return {"status": "ok"}
