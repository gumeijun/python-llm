"""
配置文件
"""
import os
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"

# 服务器配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# 模型配置
DEFAULT_MODEL_TYPE = "auto"
DEFAULT_MAX_LENGTH = 32768
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_DO_SAMPLE = True

# GPU配置
USE_GPU = os.getenv("USE_GPU", "True").lower() == "true"
GPU_MEMORY_FRACTION = float(os.getenv("GPU_MEMORY_FRACTION", "0.8"))

# 下载配置
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 300))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 安全配置
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# 推荐的模型列表
RECOMMENDED_MODELS = [
    {
        "name": "microsoft/DialoGPT-medium",
        "type": "text-generation",
        "description": "微软的对话生成模型，适合聊天对话"
    },
    {
        "name": "gpt2",
        "type": "text-generation", 
        "description": "OpenAI的GPT-2模型，通用文本生成"
    },
    {
        "name": "t5-small",
        "type": "text2text-generation",
        "description": "Google的T5模型，支持多种NLP任务"
    },
    {
        "name": "facebook/opt-125m",
        "type": "text-generation",
        "description": "Meta的OPT模型，轻量级文本生成"
    }
]

# 模型类型映射
MODEL_TYPE_MAPPING = {
    "gpt": "text-generation",
    "bert": "text-generation", 
    "t5": "text2text-generation",
    "opt": "text-generation",
    "bloom": "text-generation",
    "llama": "text-generation"
}