from fastapi import FastAPI
from app.routes.gateway import router
from app.security.persistence import init_db
from app.config import settings
from app.middleware.telemetry import TelemetryMiddleware
from loguru import logger
import sys

# Configure Loguru logging
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:<8}</level> | {message}")

app = FastAPI(
    title="InsightBridge API Gateway",
    version="4.2",
    description="Security-Hardened API Gateway for Sovereign Core",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(TelemetryMiddleware)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing InsightBridge v4.2...")

    try:
        init_db()
        logger.info("Security Persistence Layer initialized successfully.")
    except Exception as exc:
        logger.critical(f"FATAL: Database initialization failed: {exc}")
        sys.exit(1)

    if settings.JWT_SECRET == "change-me":
        logger.critical("FATAL: Default JWT_SECRET detected. Service will not start in production mode.")
        if not settings.DEBUG:
            sys.exit(1)

    logger.info("InsightBridge is READY. Listening for ingest requests.")

app.include_router(router, tags=["Gateway"])

@app.get("/")
def root():
    return {
        "message": "InsightBridge API is running",
        "status": "OK",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "4.2",
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
