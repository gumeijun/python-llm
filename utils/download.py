"""
模型下载工具模块 - 支持GGUF格式模型
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from tqdm import tqdm
import requests
from huggingface_hub import hf_hub_download, list_repo_files
import logging

logger = logging.getLogger(__name__)


class ModelDownloader:
    """GGUF模型下载器"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.models_info_file = self.models_dir / "models_info.json"
        self.models_info = self._load_models_info()
    
    def _load_models_info(self) -> Dict[str, Any]:
        """加载模型信息"""
        if self.models_info_file.exists():
            with open(self.models_info_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_models_info(self):
        """保存模型信息"""
        with open(self.models_info_file, 'w', encoding='utf-8') as f:
            json.dump(self.models_info, f, ensure_ascii=False, indent=2)
    
    def _find_gguf_files(self, repo_id: str) -> List[str]:
        """查找仓库中的GGUF文件"""
        try:
            files = list_repo_files(repo_id)
            gguf_files = [f for f in files if f.endswith('.gguf')]
            return gguf_files
        except Exception as e:
            logger.error(f"查找GGUF文件失败: {str(e)}")
            return []
    
    def _select_best_gguf_file(self, gguf_files: List[str]) -> str:
        """选择最佳的GGUF文件"""
        if not gguf_files:
            raise ValueError("未找到GGUF文件")
        
        # 优先级：Q4_0 > Q4_1 > Q8_0 > F16 > F32
        priority_order = ['q4_0', 'q4_1', 'q8_0', 'f16', 'f32']
        
        for priority in priority_order:
            for file in gguf_files:
                if priority in file.lower():
                    return file
        
        # 如果没有找到优先级文件，返回第一个
        return gguf_files[0]
    
    def download_model(self, model_name: str, model_type: str = "auto") -> Dict[str, Any]:
        """
        下载GGUF格式模型
        
        Args:
            model_name: 模型名称（Hugging Face Hub格式）
            model_type: 模型类型（auto, text-generation等）
            
        Returns:
            模型信息字典
        """
        print(f"开始下载GGUF模型: {model_name}")
        
        # 检查模型是否已存在
        if model_name in self.models_info:
            model_info = self.models_info[model_name]
            if Path(model_info["path"]).exists():
                print(f"模型 {model_name} 已存在")
                return model_info
        
        try:
            # 查找GGUF文件
            print("正在查找GGUF文件...")
            gguf_files = self._find_gguf_files(model_name)
            
            if not gguf_files:
                raise ValueError(f"在仓库 {model_name} 中未找到GGUF文件")
            
            # 选择最佳的GGUF文件
            selected_file = self._select_best_gguf_file(gguf_files)
            print(f"选择文件: {selected_file}")
            
            # 创建模型目录
            model_dir = self.models_dir / model_name.replace("/", "_")
            model_dir.mkdir(exist_ok=True)
            
            # 下载GGUF文件
            print(f"正在下载 {selected_file}...")
            local_file_path = hf_hub_download(
                repo_id=model_name,
                filename=selected_file,
                local_dir=str(model_dir)
            )
            
            # 获取模型信息
            model_info = {
                "name": model_name,
                "type": "gguf",
                "path": local_file_path,
                "gguf_file": selected_file,
                "available_files": gguf_files,
                "status": "ready"
            }
            
            # 保存模型信息
            self.models_info[model_name] = model_info
            self._save_models_info()
            
            print(f"模型 {model_name} 下载完成")
            return model_info
            
        except Exception as e:
            print(f"下载模型 {model_name} 时出错: {str(e)}")
            # 清理失败的下载
            model_dir = self.models_dir / model_name.replace("/", "_")
            if model_dir.exists():
                import shutil
                shutil.rmtree(model_dir)
            raise
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """获取模型信息"""
        return self.models_info.get(model_name)
    
    def list_models(self) -> Dict[str, Any]:
        """列出所有已下载的模型"""
        return self.models_info
    
    def delete_model(self, model_name: str) -> bool:
        """删除模型"""
        if model_name not in self.models_info:
            return False
        
        model_info = self.models_info[model_name]
        model_path = Path(model_info["path"])
        
        # 删除整个模型目录
        model_dir = model_path.parent
        if model_dir.exists():
            import shutil
            shutil.rmtree(model_dir)
        
        del self.models_info[model_name]
        self._save_models_info()
        return True
    
    def check_model_status(self, model_name: str) -> str:
        """检查GGUF模型状态"""
        if model_name not in self.models_info:
            return "not_found"
        
        model_info = self.models_info[model_name]
        model_path = Path(model_info["path"])
        
        if not model_path.exists():
            return "corrupted"
        
        # 检查是否为GGUF文件
        if not model_path.name.endswith('.gguf'):
            return "invalid_format"
        
        # 检查文件大小（GGUF文件通常较大）
        if model_path.stat().st_size < 1024:  # 小于1KB可能是损坏的
            return "incomplete"
        
        return "ready"