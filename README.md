# Python LLM - 本地大语言模型服务

一个轻量级的本地大语言模型服务，类似Ollama，支持GGUF格式模型的拉取、管理和推理。

## 🌟 特性

- **🚀 快速部署**: 一键启动，无需复杂配置
- **📦 GGUF支持**: 原生支持量化GGUF格式模型
- **🎯 多接口**: 支持API、CLI和Web界面
- **⚡ 硬件加速**: 自动检测并使用Metal (macOS) 或CUDA (Linux/Windows)
- **🔄 流式响应**: 支持流式文本生成
- **💾 内存优化**: 智能模型加载和内存管理

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd python-llm

# 安装依赖
pip install -r requirements.txt
```

### 启动服务

```bash
# 启动API服务
python main.py

# 或使用启动脚本
./start.sh
```

服务将在 http://localhost:8000 启动，可访问 /docs 查看API文档。

### 命令行使用

```bash
# 拉取模型
./llm pull microsoft/Phi-3-mini-4k-instruct-gguf

# 列出模型
./llm list

# 运行交互式聊天
./llm run microsoft/Phi-3-mini-4k-instruct-gguf

# 单次文本生成
./llm generate microsoft/Phi-3-mini-4k-instruct-gguf "你好，请介绍机器学习"
```

## 📖 详细使用

### API接口

#### 1. 拉取模型
```bash
curl -X POST "http://localhost:8000/models/pull" \
     -H "Content-Type: application/json" \
     -d '{"model_name": "microsoft/Phi-3-mini-4k-instruct-gguf"}'
```

#### 2. 文本生成
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "model_name": "microsoft/Phi-3-mini-4k-instruct-gguf",
       "prompt": "你好",
       "max_tokens": 512,
       "temperature": 0.7
     }'
```

#### 3. 聊天补全
```bash
curl -X POST "http://localhost:8000/generate/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "model_name": "microsoft/Phi-3-mini-4k-instruct-gguf",
       "messages": [
         {"role": "user", "content": "你好"}
       ],
       "max_tokens": 512
     }'
```

### 推荐模型

| 模型名称 | 大小 | 适用场景 |
|----------|------|----------|
| `microsoft/Phi-3-mini-4k-instruct-gguf` | 2.4GB | 通用对话 |
| `Qwen/Qwen2-1.5B-Instruct-GGUF` | 3.2GB | 中文对话 |
| `unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF` | 1.5GB | 轻量级推理 |
| `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF` | 8GB | 高质量推理 |

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `HOST` | 0.0.0.0 | 服务监听地址 |
| `PORT` | 8000 | 服务端口 |
| `USE_GPU` | True | 是否使用GPU加速 |
| `LOG_LEVEL` | INFO | 日志级别 |

## 🏗️ 项目结构

```
python-llm/
├── main.py              # 主程序入口
├── model_manager.py     # 模型管理器
├── inference.py         # 推理引擎
├── config.py           # 配置文件
├── llm.py              # 命令行工具
├── llm                 # 命令行入口脚本
├── api/                # API模块
│   ├── __init__.py
│   ├── models.py       # 模型管理API
│   └── generate.py     # 文本生成API
├── utils/              # 工具模块
│   ├── __init__.py
│   └── download.py     # 模型下载器
├── models/             # 模型存储目录
│   └── models_info.json # 模型信息文件
└── requirements.txt    # 依赖列表
```

## 🔧 开发指南

### 添加新功能

1. **添加新的API端点**: 在 `api/` 目录下创建新的路由文件
2. **扩展模型支持**: 修改 `utils/download.py` 中的模型选择逻辑
3. **自定义配置**: 在 `config.py` 中添加新的配置项

### 调试模式

```bash
# 开启调试模式
export DEBUG=true
python main.py

# 查看详细日志
export LOG_LEVEL=DEBUG
python main.py
```

## 🐛 常见问题

### 模型下载失败
- **检查网络**: 确保能访问huggingface.co
- **代理设置**: 设置HTTP_PROXY/HTTPS_PROXY环境变量
- **重试**: 删除models目录下的对应文件夹后重试

### 内存不足
- **使用小模型**: 选择1.5B或更小的模型
- **量化模型**: 使用Q4_0或Q8_0量化版本
- **关闭GPU**: 设置USE_GPU=false使用CPU

### 推理速度慢
- **检查设备**: 查看日志确认是否使用了GPU加速
- **模型缓存**: 首次加载较慢，后续会缓存
- **调整参数**: 减少max_tokens或使用更快的采样参数

## 📄 许可证

MIT License - 详见LICENSE文件

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请通过以下方式获取帮助：
1. 查看项目文档
2. 运行测试脚本
3. 提交GitHub Issue
