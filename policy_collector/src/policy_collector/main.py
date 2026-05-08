"""FastAPI 应用入口"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .api import policies_router, customer_actions_router
from .config import get_settings
from .database import init_db, close_db
from .core.vector_client import VectorClient

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    await init_db()
    logger.info("Database initialized")

    await _init_vector_db()

    yield

    await close_db()
    logger.info("Database connection closed")


async def _init_vector_db() -> None:
    """初始化向量数据库"""
    try:
        client = VectorClient()
        await client.create_collection(force_recreate=False)
        logger.info(f"Vector collection '{settings.collection_name}' ready")
    except Exception as e:
        logger.warning(f"Vector DB initialization failed (will retry on first use): {e}")


app = FastAPI(
    title="政策搜集智能体系统",
    description="PolicyCollector - 精准政策匹配与溯源",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(policies_router)
app.include_router(customer_actions_router)

# Mount demo static files
demo_path = Path(__file__).parent.parent.parent.parent / "demo"
if demo_path.exists():
    app.mount("/demo", StaticFiles(directory=str(demo_path), html=True), name="demo")


@app.get("/", tags=["健康检查"])
async def root():
    """根路径"""
    return {
        "name": "政策搜集智能体系统",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.log_level == "DEBUG" else None,
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "policy_collector.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
