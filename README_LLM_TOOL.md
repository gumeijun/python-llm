# Python LLM - 类似 Ollama 的简洁工具

一个类似 Ollama 的简洁命令行工具，支持在本地运行大型语言模型，特别优化了 M1/M2 芯片的性能。

## 🚀 快速开始

### 运行交互模式 (类似 `ollama run`)
```bash
./llm run microsoft/phi-2
```

### 单次文本生成
```bash
./llm generate microsoft/phi-2 "你好，请介绍一下人工智能"
```

### 列出可用模型
```bash
./llm list
```

### 拉取模型信息
```bash
./llm pull microsoft/phi-2
```

## 📋 支持的模型

- `microsoft/phi-2` - 微软的 Phi-2 模型 (推荐)
- `gpt2` - OpenAI GPT-2 基础模型
- `gpt2-medium` - GPT-2 中等规模模型
- `gpt2-large` - GPT-2 大规模模型

## 💬 交互模式命令

在交互模式中，您可以使用以下命令：

- `/exit` - 退出程序
- `/help` - 显示帮助信息
- `/clear` - 清屏
- 其他输入 - 与AI对话

## 🔧 特性

### M1/M2 芯片优化
- ✅ 自动检测并使用 MPS (Metal Performance Shaders) 加速
- ✅ 智能回退机制：MPS → CPU
- ✅ 兼容性检测和警告

### 设备支持优先级
1. **MPS** (M1/M2 芯片) - 最优性能
2. **CUDA** (NVIDIA GPU) - 高性能
3. **CPU** - 兼容性保证

### 用户体验
- 🎯 简洁的命令行界面
- ⚡ 实时显示生成时间和设备信息
- 🔄 自动错误处理和回退
- 📊 详细的性能统计

## 📖 使用示例

### 示例 1: 启动交互对话
```bash
$ ./llm run microsoft/phi-2
🚀 启动 microsoft/phi-2 交互模式
==================================================
🔧 设备: mps
📱 MPS: True
🖥️ CUDA: False

⏳ 加载模型...
✅ 模型加载成功 (15.2秒)
🎯 使用设备: mps

💬 进入对话模式 (输入 /exit 退出, /help 查看帮助)
--------------------------------------------------

👤 您: 你好
🤖 AI: 你好！我是一个AI助手，很高兴与您对话。有什么我可以帮助您的吗？
⚡ (2.1秒, mps)
```

### 示例 2: 单次生成
```bash
$ ./llm generate microsoft/phi-2 "解释什么是机器学习" --max-length 200
🚀 使用 microsoft/phi-2 生成文本
📝 提示: 解释什么是机器学习
--------------------------------------------------
🤖 生成结果:
机器学习是人工智能的一个分支，它使计算机能够在没有明确编程的情况下学习和改进...

⚡ 设备: mps
```

## ⚠️ 注意事项

1. **首次使用**: 模型会在首次使用时自动从 Hugging Face 下载
2. **网络连接**: 首次下载需要稳定的网络连接
3. **存储空间**: 确保有足够的磁盘空间存储模型文件
4. **MPS 兼容性**: 在某些 macOS 版本上可能会自动回退到 CPU

## 🛠️ 技术实现

- **推理引擎**: 基于 `M1OptimizedInferenceEngine`
- **模型加载**: 使用 Transformers 库
- **设备管理**: 智能设备检测和切换
- **错误处理**: 自动回退和错误恢复

## 📁 相关文件

- `llm` - 主启动脚本
- `cli.py` - 命令行界面实现
- `m1_inference.py` - M1 优化推理引擎
- `inference.py` - 通用推理引擎

---

**享受与AI的对话吧！** 🤖✨