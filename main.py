"""
Python LLM - 类似Ollama的本地大语言模型服务
主程序入口
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import router as models_router
from api.generate import router as generate_router
from model_manager import ModelManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Python LLM",
    description="类似Ollama的本地大语言模型服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(models_router)
app.include_router(generate_router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Python LLM 服务正在运行",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "models": "/models",
            "generate": "/generate"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 检查模型管理器是否正常工作
        model_manager = ModelManager()
        models = model_manager.list_models()
        
        return {
            "status": "healthy",
            "models_count": models["total"],
            "loaded_models_count": len(model_manager.get_loaded_models())
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        raise HTTPException(status_code=500, detail="服务异常")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"未处理的异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "内部服务器错误", "detail": str(exc)}
    )


def main():
    """主函数"""
    logger.info("启动 Python LLM 服务...")
    
    # 启动服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main() 