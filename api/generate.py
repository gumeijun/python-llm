"""
文本生成API模块
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from model_manager import ModelManager

router = APIRouter(prefix="/generate", tags=["文本生成"])

# 全局模型管理器实例
model_manager = ModelManager()


class GenerateRequest(BaseModel):
    """文本生成请求"""
    model_name: str
    prompt: str
    max_tokens: int = 32768
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    num_return_sequences: int = 1


class GenerateResponse(BaseModel):
    """文本生成响应"""
    success: bool
    generated_text: Optional[str] = None
    prompt: Optional[str] = None
    model_name: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    生成文本
    
    - **model_name**: 模型名称
    - **prompt**: 输入提示
    - **max_tokens**: 最大生成token数量（默认100）
    - **temperature**: 温度参数（默认0.7）
    - **top_p**: top-p采样参数（默认0.9）
    - **top_k**: top-k采样参数（默认40）
    - **repeat_penalty**: 重复惩罚（默认1.1）
    - **num_return_sequences**: 返回序列数量（默认1）
    """
    try:
        result = model_manager.generate_text(
            model_name=request.model_name,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            repeat_penalty=request.repeat_penalty,
            num_return_sequences=request.num_return_sequences
        )
        
        if "error" in result:
            return GenerateResponse(
                success=False,
                error=result["error"]
            )
        
        return GenerateResponse(
            success=True,
            generated_text=result["generated_text"],
            prompt=result["prompt"],
            model_name=result["model_name"],
            parameters=result["parameters"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def generate_text_stream(request: GenerateRequest):
    """
    流式生成文本（实验性功能）
    
    注意：这是一个简化的流式实现，实际应用中可能需要更复杂的处理
    """
    try:
        # 这里可以实现真正的流式生成
        # 目前返回普通生成结果
        result = model_manager.generate_text(
            model_name=request.model_name,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            repeat_penalty=request.repeat_penalty
        )
        
        if "error" in result:
            yield {"error": result["error"]}
            return
        
        # 模拟流式输出
        generated_text = result["generated_text"]
        words = generated_text.split()
        
        for i, word in enumerate(words):
            yield {
                "type": "token",
                "content": word + (" " if i < len(words) - 1 else ""),
                "finished": i == len(words) - 1
            }
        
        yield {
            "type": "complete",
            "full_text": generated_text,
            "parameters": result["parameters"]
        }
        
    except Exception as e:
        yield {"error": str(e)}


@router.get("/models")
async def get_available_models():
    """获取可用于生成的模型列表"""
    try:
        models = model_manager.list_models()
        available_models = []
        
        for model_name, model_info in models["models"].items():
            if model_info["status"] == "ready":
                available_models.append({
                    "name": model_name,
                    "type": model_info["type"],
                    "loaded": model_info["loaded"]
                })
        
        return {
            "success": True,
            "data": {
                "models": available_models,
                "total": len(available_models)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))