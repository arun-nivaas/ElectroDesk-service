from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.v1.router import v1_router
from src.backend.core.logger import logger
from src.backend.core.constants import constant
from typing import Dict, Any
from src.backend.database.init_db import init_db
from src.backend.scheduler.keep_alive import KeepAlive
from src.backend.core.config import settings
from contextlib import asynccontextmanager
import uvicorn
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = None
    if settings.APP_ENV == "production" and settings.RENDER_URL:
        keep_alive_service = KeepAlive(settings.RENDER_URL)
        task = asyncio.create_task(keep_alive_service.start())
    
    yield
    if task:
        task.cancel()


app = FastAPI(
    title=f"{constant.APP_TITLE} API",
    version=constant.API_VERSION,
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_ENV != "production" else [settings.RENDER_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=f"{constant.API_PREFIX}") 

@app.get("/health", status_code=status.HTTP_200_OK)
async def root_health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": constant.APP_TITLE,
        "version": constant.APP_VERSION,
        "environment": settings.APP_ENV,
        "documentation": "/docs" if settings.APP_ENV != "production" else "disabled",
        "message": "API is operational. Use /docs for API documentation."
    }

if __name__ == "__main__":
    
    logger.info(f"🌐 Starting server on http://{constant.HOST}:{constant.PORT}")
    logger.info(f"📚 API docs available at http://{constant.HOST}:{constant.PORT}/docs")
    logger.info(f"🔧 Environment: {settings.APP_ENV}")

    uvicorn.run(
        "main:app",
        host=constant.HOST,
        port=constant.PORT,
        reload=settings.APP_ENV != "production",
        log_level="debug" if settings.APP_ENV != "production" else "info"
    )
