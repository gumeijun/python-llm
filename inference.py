"""
基于 llama.cpp 的推理引擎模块
"""
import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    from llama_cpp import Llama
except ImportError:
    raise ImportError("请安装 llama-cpp-python: pip install llama-cpp-python")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InferenceEngine:
    """基于 llama.cpp 的推理引擎"""
    
    def __init__(self, n_ctx: int = 2048, n_threads: Optional[int] = None):
        """
        初始化推理引擎
        
        Args:
            n_ctx: 上下文长度
            n_threads: 线程数，None表示自动检测
        """
        self.loaded_models = {}
        self.n_ctx = n_ctx
        self.n_threads = n_threads or os.cpu_count()
        
        # 检测设备能力
        self.device_info = self._detect_device_capabilities()
        logger.info(f"推理引擎初始化完成，线程数: {self.n_threads}, 上下文长度: {n_ctx}")
    
    def _detect_device_capabilities(self) -> Dict[str, Any]:
        """检测设备能力"""
        info = {
            "cpu_count": os.cpu_count(),
            "supports_gpu": False,
            "supports_metal": False
        }
        
        # 检测GPU支持（CUDA/OpenCL）
        try:
            # 这里可以添加GPU检测逻辑
            pass
        except:
            pass
        
        # 检测Metal支持（macOS）
        try:
            import platform
            if platform.system() == "Darwin":
                info["supports_metal"] = True
        except:
            pass
        
        return info
    
    def load_model(self, model_path: str, **kwargs) -> bool:
        """
        加载GGUF格式的模型
        
        Args:
            model_path: 模型文件路径（.gguf文件）
            **kwargs: 额外的llama.cpp参数
            
        Returns:
            是否加载成功
        """
        try:
            # 检查模型文件是否存在
            if not os.path.exists(model_path):
                logger.error(f"模型文件不存在: {model_path}")
                return False
            
            # 检查文件扩展名
            if not model_path.lower().endswith(('.gguf', '.ggml')):
                logger.warning(f"模型文件可能不是GGUF/GGML格式: {model_path}")
            
            logger.info(f"正在加载模型: {model_path}")
            
            # 设置默认参数
            llama_kwargs = {
                "model_path": model_path,
                "n_ctx": self.n_ctx,
                "n_threads": self.n_threads,
                "verbose": False,
                **kwargs
            }
            
            # 根据设备能力调整参数
            if self.device_info.get("supports_metal"):
                llama_kwargs["n_gpu_layers"] = -1  # 使用Metal加速
                logger.info("启用Metal GPU加速")
            
            # 创建Llama实例
            llama_model = Llama(**llama_kwargs)
            
            self.loaded_models[model_path] = {
                "model": llama_model,
                "model_path": model_path,
                "n_ctx": self.n_ctx,
                "load_params": llama_kwargs
            }
            
            logger.info(f"模型 {model_path} 加载成功")
            return True
            
        except Exception as e:
            logger.error(f"加载模型 {model_path} 时出错: {str(e)}")
            return False
    
    def unload_model(self, model_path: str) -> bool:
        """卸载模型"""
        if model_path in self.loaded_models:
            # llama.cpp会自动清理资源
            del self.loaded_models[model_path]
            logger.info(f"模型 {model_path} 已卸载")
            return True
        return False
    
    def is_model_loaded(self, model_path: str) -> bool:
        """检查模型是否已加载"""
        return model_path in self.loaded_models
    
    def generate_text(
        self, 
        model_path: str, 
        prompt: str, 
        max_tokens: int = 32768,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        repeat_penalty: float = 1.1,
        stop: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成文本
        
        Args:
            model_path: 模型路径
            prompt: 输入提示
            max_tokens: 最大生成token数
            temperature: 温度参数
            top_p: top-p采样参数
            top_k: top-k采样参数
            repeat_penalty: 重复惩罚
            stop: 停止词列表
            
        Returns:
            生成结果
        """
        if not self.is_model_loaded(model_path):
            if not self.load_model(model_path):
                return {"error": "模型加载失败"}
        
        try:
            model_info = self.loaded_models[model_path]
            llama_model = model_info["model"]
            
            # 设置停止词
            if stop is None:
                stop = ["</s>", "<|endoftext|>", "\n\n"]
            
            logger.info(f"开始生成文本，提示: {prompt[:50]}...")
            
            # 生成文本
            output = llama_model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repeat_penalty=repeat_penalty,
                stop=stop,
                echo=False,  # 不回显输入
                **kwargs
            )
            
            generated_text = output["choices"][0]["text"]
            
            return {
                "generated_text": generated_text,
                "prompt": prompt,
                "model_path": model_path,
                "parameters": {
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "repeat_penalty": repeat_penalty
                },
                "usage": output.get("usage", {}),
                "finish_reason": output["choices"][0].get("finish_reason")
            }
            
        except Exception as e:
            logger.error(f"生成文本时出错: {str(e)}")
            return {"error": str(e)}
    
    def get_model_info(self, model_path: str) -> Optional[Dict[str, Any]]:
        """获取已加载模型的信息"""
        if model_path in self.loaded_models:
            model_info = self.loaded_models[model_path]
            return {
                "path": model_path,
                "n_ctx": model_info["n_ctx"],
                "device_info": self.device_info,
                "load_params": model_info["load_params"]
            }
        return None
    
    def list_loaded_models(self) -> List[str]:
        """列出已加载的模型"""
        return list(self.loaded_models.keys())
    
    def clear_all_models(self):
        """清除所有已加载的模型"""
        self.loaded_models.clear()
        logger.info("所有模型已清除")
    
    def chat_completion(
        self,
        model_path: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 32768,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        聊天补全接口（类似OpenAI API）
        
        Args:
            model_path: 模型路径
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Returns:
            聊天补全结果
        """
        if not self.is_model_loaded(model_path):
            if not self.load_model(model_path):
                return {"error": "模型加载失败", "success": False}
        
        try:
            model_info = self.loaded_models[model_path]
            llama_model = model_info["model"]
            
            # 使用llama.cpp的chat completion功能
            response = llama_model.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            # 提取生成的文本
            if response and "choices" in response and len(response["choices"]) > 0:
                generated_text = response["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "response": generated_text,
                    "model_path": model_path,
                    "usage": response.get("usage", {}),
                    "finish_reason": response["choices"][0].get("finish_reason")
                }
            else:
                return {"error": "生成响应为空", "success": False}
            
        except Exception as e:
            logger.error(f"聊天补全时出错: {str(e)}")
            return {"error": str(e), "success": False}
    
    def chat_completion_stream(
        self,
        model_path: str,
        messages: List[Dict[str, str]],
        max_tokens: int = 100,
        temperature: float = 0.7,
        **kwargs
    ):
        """
        流式聊天补全接口
        
        Args:
            model_path: 模型路径
            messages: 消息列表，格式: [{"role": "user", "content": "..."}]
            max_tokens: 最大生成token数
            temperature: 温度参数
            
        Yields:
            流式生成的文本片段
        """
        if not self.is_model_loaded(model_path):
            if not self.load_model(model_path):
                yield {"error": "模型加载失败", "success": False}
                return
        
        try:
            model_info = self.loaded_models[model_path]
            llama_model = model_info["model"]

            
            # 使用llama.cpp的流式chat completion功能
            stream = llama_model.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
                **kwargs
            )
            
            full_response = ""
            for chunk in stream:
                if chunk and "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    if "content" in delta:
                        content = delta["content"]
                        full_response += content
                        yield {
                            "success": True,
                            "content": content,
                            "full_response": full_response,
                            "finish_reason": chunk["choices"][0].get("finish_reason")
                        }
            
            # 最后返回完整响应
            yield {
                "success": True,
                "content": "",
                "full_response": full_response,
                "finish_reason": "stop",
                "done": True
            }
            
        except Exception as e:
            logger.error(f"流式聊天补全时出错: {str(e)}")
            yield {"error": str(e), "success": False}