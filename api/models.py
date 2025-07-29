"""
模型管理API模块
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from model_manager import ModelManager

router = APIRouter(prefix="/models", tags=["模型管理"])

# 全局模型管理器实例
model_manager = ModelManager()


class PullModelRequest(BaseModel):
    """拉取模型请求"""
    model_name: str
    model_type: str = "auto"


class ModelResponse(BaseModel):
    """模型响应"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


@router.post("/pull", response_model=ModelResponse)
async def pull_model(request: PullModelRequest):
    """
    拉取模型
    
    - **model_name**: 模型名称（Hugging Face Hub格式）
    - **model_type**: 模型类型（可选，默认为auto）
    """
    try:
        result = model_manager.pull_model(request.model_name, request.model_type)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return ModelResponse(
            success=True,
            message=result.get("message", "模型拉取成功"),
            data=result.get("model_info")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_models():
    """列出所有已下载的模型"""
    try:
        result = model_manager.list_models()
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """获取指定模型的信息"""
    try:
        model_info = model_manager.get_model_info(model_name)
        if not model_info:
            raise HTTPException(status_code=404, detail="模型不存在")
        
        return {
            "success": True,
            "data": model_info
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/load")
async def load_model(model_name: str):
    """加载模型到内存"""
    try:
        result = model_manager.load_model(model_name)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": result.get("message", "模型加载成功"),
            "data": result.get("model_info")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{model_name}/unload")
async def unload_model(model_name: str):
    """卸载模型"""
    try:
        result = model_manager.unload_model(model_name)
        return {
            "success": True,
            "message": result.get("message", "模型卸载成功")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{model_name}")
async def delete_model(model_name: str):
    """删除模型"""
    try:
        result = model_manager.delete_model(model_name)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": result.get("message", "模型删除成功")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/loaded/list")
async def list_loaded_models():
    """列出已加载的模型"""
    try:
        loaded_models = model_manager.get_loaded_models()
        return {
            "success": True,
            "data": {
                "models": loaded_models,
                "total": len(loaded_models)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear")
async def clear_all_models():
    """清除所有已加载的模型"""
    try:
        result = model_manager.clear_all_models()
        return {
            "success": True,
            "message": result.get("message", "所有模型已清除")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 