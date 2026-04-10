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

# Create database tables
Base.metadata.create_all(bind=engine)

# Load environment variables
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


app = FastAPI(
    title=f"{constant.APP_TITLE} API",
    version=constant.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
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
