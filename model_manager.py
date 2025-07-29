"""
模型管理器模块
"""
from typing import Dict, Any, Optional, List
from utils.download import ModelDownloader
from inference import InferenceEngine
import logging

logger = logging.getLogger(__name__)


class ModelManager:
    """模型管理器"""
    
    def __init__(self, models_dir: str = "models"):
        self.downloader = ModelDownloader(models_dir)
        self.inference_engine = InferenceEngine()
    
    def pull_model(self, model_name: str, model_type: str = "auto") -> Dict[str, Any]:
        """
        拉取模型
        
        Args:
            model_name: 模型名称
            model_type: 模型类型
            
        Returns:
            模型信息
        """
        try:
            # 下载模型
            model_info = self.downloader.download_model(model_name, model_type)
            
            # 检查模型状态
            status = self.downloader.check_model_status(model_name)
            if status != "ready":
                return {
                    "error": f"模型状态异常: {status}",
                    "model_info": model_info
                }
            
            return {
                "success": True,
                "model_info": model_info,
                "message": f"模型 {model_name} 拉取成功"
            }
            
        except Exception as e:
            logger.error(f"拉取模型 {model_name} 时出错: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    def list_models(self) -> Dict[str, Any]:
        """列出所有模型"""
        models = self.downloader.list_models()
        
        # 添加模型状态信息
        for model_name, model_info in models.items():
            status = self.downloader.check_model_status(model_name)
            model_info["status"] = status
            model_info["loaded"] = self.inference_engine.is_model_loaded(model_info["path"])
        
        return {
            "models": models,
            "total": len(models)
        }
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取模型信息"""
        model_info = self.downloader.get_model_info(model_name)
        if model_info:
            status = self.downloader.check_model_status(model_name)
            model_info["status"] = status
            model_info["loaded"] = self.inference_engine.is_model_loaded(model_info["path"])
        return model_info
    
    def load_model(self, model_name: str) -> Dict[str, Any]:
        """加载模型到内存"""
        model_info = self.downloader.get_model_info(model_name)
        if not model_info:
            return {"error": "模型不存在"}
        
        status = self.downloader.check_model_status(model_name)
        if status != "ready":
            return {"error": f"模型状态异常: {status}"}
        
        if self.inference_engine.is_model_loaded(model_info["path"]):
            return {"message": "模型已加载", "model_info": model_info}
        
        success = self.inference_engine.load_model(model_info["path"])
        if success:
            return {
                "success": True,
                "message": f"模型 {model_name} 加载成功",
                "model_info": model_info
            }
        else:
            return {"error": "模型加载失败"}
    
    def unload_model(self, model_name: str) -> Dict[str, Any]:
        """卸载模型"""
        model_info = self.downloader.get_model_info(model_name)
        if not model_info:
            return {"error": "模型不存在"}
        
        success = self.inference_engine.unload_model(model_info["path"])
        if success:
            return {"message": f"模型 {model_name} 卸载成功"}
        else:
            return {"message": "模型未加载"}
    
    def delete_model(self, model_name: str) -> Dict[str, Any]:
        """删除模型"""
        # 先卸载模型
        self.unload_model(model_name)
        
        # 删除模型文件
        success = self.downloader.delete_model(model_name)
        if success:
            return {"message": f"模型 {model_name} 删除成功"}
        else:
            return {"error": "模型不存在或删除失败"}
    
    def generate_text(
        self, 
        model_name: str, 
        prompt: str, 
        max_tokens: int = 32768,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        repeat_penalty: float = 1.1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成文本
        
        Args:
            model_name: 模型名称
            prompt: 输入提示
            max_tokens: 最大生成token数
            temperature: 温度参数
            top_p: top-p采样参数
            top_k: top-k采样参数
            repeat_penalty: 重复惩罚
            
        Returns:
            生成结果
        """
        model_info = self.downloader.get_model_info(model_name)
        if not model_info:
            return {"error": "模型不存在"}
        
        status = self.downloader.check_model_status(model_name)
        if status != "ready":
            return {"error": f"模型状态异常: {status}"}
        
        # 确保模型已加载
        if not self.inference_engine.is_model_loaded(model_info["path"]):
            load_result = self.load_model(model_name)
            if "error" in load_result:
                return load_result
        
        # 生成文本
        result = self.inference_engine.generate_text(
            model_info["path"],
            prompt,
            max_tokens,
            temperature,
            top_p,
            top_k,
            repeat_penalty,
            **kwargs
        )
        
        if "error" in result:
            return result
        
        # 添加模型信息
        result["model_name"] = model_name
        return result
    
    def chat_completion(
        self,
        model_name: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 32768,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        聊天补全接口
        
        Args:
            model_name: 模型名称
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Returns:
            聊天补全结果
        """
        model_info = self.downloader.get_model_info(model_name)
        if not model_info:
            return {"error": "模型不存在"}
        
        status = self.downloader.check_model_status(model_name)
        if status != "ready":
            return {"error": f"模型状态异常: {status}"}
        
        # 确保模型已加载
        if not self.inference_engine.is_model_loaded(model_info["path"]):
            load_result = self.load_model(model_name)
            if "error" in load_result:
                return load_result
        
        # 聊天补全
        result = self.inference_engine.chat_completion(
            model_info["path"],
            messages,
            max_tokens,
            temperature,
            **kwargs
        )
        
        if "error" in result:
            return result
        
        # 添加模型信息
        result["model"] = model_name
        return result
    
    def chat_completion_stream(
        self,
        model_name: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 32768,
        temperature: float = 0.7,
        **kwargs
    ):
        """
        流式聊天补全接口
        
        Args:
            model_name: 模型名称
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Yields:
            流式聊天补全结果
        """
        model_info = self.downloader.get_model_info(model_name)
        if not model_info:
            yield {"error": "模型不存在"}
            return
        
        status = self.downloader.check_model_status(model_name)
        if status != "ready":
            yield {"error": f"模型状态异常: {status}"}
            return
        
        # 确保模型已加载
        if not self.inference_engine.is_model_loaded(model_info["path"]):
            load_result = self.load_model(model_name)
            if "error" in load_result:
                yield load_result
                return
        
        # 流式聊天补全
        for chunk in self.inference_engine.chat_completion_stream(
            model_info["path"],
            messages,
            max_tokens,
            temperature,
            **kwargs
        ):
            if "error" in chunk:
                yield chunk
                return
            
            # 添加模型信息
            chunk["model"] = model_name
            yield chunk

    def get_loaded_models(self) -> List[Dict[str, Any]]:
        """获取已加载的模型列表"""
        loaded_models = []
        for model_path in self.inference_engine.list_loaded_models():
            model_info = self.inference_engine.get_model_info(model_path)
            if model_info:
                loaded_models.append(model_info)
        return loaded_models
    
    def clear_all_models(self):
        """清除所有已加载的模型"""
        self.inference_engine.clear_all_models()
        return {"message": "所有模型已清除"}