from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware
from src.backend.api.v1.router import v1_router
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
from src.backend.core.logger import logger
from src.backend.core.constants import constant
from typing import Dict, Any
from src.backend.database import Base, engine
from contextlib import asynccontextmanager
import asyncio
import httpx
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Load environment variables
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

RENDER_URL = os.getenv("RENDER_URL", "")

async def keep_alive():
    """Pings the app every 10 minutes to prevent Render sleep"""
    await asyncio.sleep(60)  # wait 1 minute after startup first
    while True:
        try:
            if RENDER_URL:
                async with httpx.AsyncClient() as client:
                    await client.get(f"{RENDER_URL}/health")
                    print(f"Keep alive ping sent to {RENDER_URL}/health")
        except Exception as e:
            print(f"Keep alive ping failed: {e}")
        await asyncio.sleep(600)  # ping every 10 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(keep_alive())
    yield
    task.cancel()


app = FastAPI(
    title=f"{constant.APP_TITLE} API",
    version=constant.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(v1_router,prefix=f"{constant.API_PREFIX}/voice",tags=[f"Billing service {constant.API_VERSION}"])
app.include_router(v1_router, prefix=f"{constant.API_PREFIX}") 

# Health check endpoint
@app.get("/health", status_code = status.HTTP_200_OK)
async def root_health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": constant.APP_TITLE,
        "version": constant.APP_VERSION,
        "documentation": "/docs",
        "message": "API is operational. Use /docs for API documentation."
    }

if __name__ == "__main__":
    
    logger.info(f"🌐 Starting server on http://{constant.HOST}:{constant.PORT}")
    logger.info(f"📚 API docs available at http://{constant.HOST}:{constant.PORT}/docs\n")

    uvicorn.run("main:app", host=constant.HOST, port=constant.PORT, reload=True, log_level="info")
