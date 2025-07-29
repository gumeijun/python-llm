# 简化的 LLM 命令行工具使用指南

## 🚀 快速开始

这是一个简化的 LLM 命令行工具，类似于 Ollama 的使用方式，支持三个核心命令：

### 📋 基本命令

```bash
# 查看帮助
./llm --help

# 列出已下载的模型
./llm list

# 拉取新模型
./llm pull <model_name>

# 运行交互式聊天
./llm run [model_name]
```

## 📖 详细使用说明

### 1. 列出模型 (`llm list`)

```bash
./llm list
```

输出示例：
```
📋 已下载的模型:
  1. Qwen/Qwen2-0.5B-Instruct-GGUF - ⭕ 未加载
     路径: models/Qwen_Qwen2-0.5B-Instruct-GGUF/qwen2-0_5b-instruct-q4_0.gguf
  2. Qwen/Qwen2-1.5B-Instruct-GGUF - ⭕ 未加载
     路径: models/Qwen_Qwen2-1.5B-Instruct-GGUF/qwen2-1_5b-instruct-q4_0.gguf
```

### 2. 拉取模型 (`llm pull`)

```bash
# 拉取 Qwen2 模型
./llm pull Qwen/Qwen2-1.5B-Instruct-GGUF

# 拉取 Phi-3 模型
./llm pull microsoft/Phi-3-mini-4k-instruct-gguf

# 拉取其他 GGUF 模型
./llm pull microsoft/DialoGPT-medium
```

### 3. 运行交互式聊天 (`llm run`)

```bash
# 使用第一个可用模型
./llm run

# 使用指定模型
./llm run Qwen/Qwen2-1.5B-Instruct-GGUF
```

交互示例：
```
🚀 启动模型: Qwen/Qwen2-1.5B-Instruct-GGUF
✅ 模型加载成功!
💬 开始聊天 (输入 'exit' 退出)
==================================================

👤 你: 你好
🤖 AI: 你好！有什么我可以帮助你的吗？

👤 你: 解释一下量子计算
🤖 AI: 量子计算是一种利用量子力学原理进行信息处理的计算方式...

👤 你: exit
👋 再见!
```

## 🎯 推荐模型

### 小型模型（快速响应）
- `Qwen/Qwen2-0.5B-Instruct-GGUF` - 0.5B 参数，适合快速对话
- `Qwen/Qwen2-1.5B-Instruct-GGUF` - 1.5B 参数，平衡性能和速度

### 中型模型（更强推理）
- `microsoft/Phi-3-mini-4k-instruct-gguf` - 微软 Phi-3，专门优化推理能力
- `microsoft/Phi-3-small-8k-instruct-gguf` - 更大的 Phi-3 模型

### 大型模型（最佳效果）
- `Qwen/Qwen2-7B-Instruct-GGUF` - 7B 参数，强大的推理能力
- `microsoft/Phi-3-medium-4k-instruct-gguf` - Phi-3 中型版本

## ⚡ 性能特性

### 🌊 流式输出
- **实时响应**: AI回复会逐字符实时显示，无需等待完整生成
- **更好体验**: 类似ChatGPT的打字机效果，提升交互体验
- **快速反馈**: 首个token延迟通常在1-2秒内
- **自动回退**: 如果流式输出失败，会自动切换到非流式模式

### ⚡ 性能优化
- **🚀 高速推理**：基于 llama.cpp，优化的 C++ 实现
- **🔧 Metal 加速**：自动启用 Apple Silicon GPU 加速
- **💾 内存优化**：GGUF 格式，量化模型减少内存占用
- **🎯 智能缓存**：模型加载缓存，避免重复加载

## 🛠️ 高级用法

### 环境变量配置

```bash
# 设置模型存储目录
export LLM_MODELS_DIR="/path/to/models"

# 设置默认模型
export LLM_DEFAULT_MODEL="Qwen/Qwen2-1.5B-Instruct-GGUF"
```

### 批量操作

```bash
# 拉取多个模型
./llm pull Qwen/Qwen2-0.5B-Instruct-GGUF
./llm pull Qwen/Qwen2-1.5B-Instruct-GGUF
./llm pull microsoft/Phi-3-mini-4k-instruct-gguf

# 查看所有模型
./llm list
```

## 🔧 故障排除

### 常见问题

1. **模型下载失败**
   ```bash
   # 检查网络连接
   ping huggingface.co
   
   # 重试下载
   ./llm pull <model_name>
   ```

2. **模型加载失败**
   ```bash
   # 检查模型文件
   ./llm list
   
   # 重新下载模型
   ./llm pull <model_name>
   ```

3. **内存不足**
   ```bash
   # 使用更小的模型
   ./llm run Qwen/Qwen2-0.5B-Instruct-GGUF
   ```

### 日志查看

程序运行时会显示详细的日志信息，包括：
- 模型加载状态
- Metal GPU 加速状态
- 推理性能指标

## 📊 与 Ollama 对比

| 功能 | 简化 LLM 工具 | Ollama |
|------|---------------|---------|
| 模型拉取 | `./llm pull` | `ollama pull` |
| 模型列表 | `./llm list` | `ollama list` |
| 交互聊天 | `./llm run` | `ollama run` |
| 模型格式 | GGUF | GGUF |
| GPU 加速 | ✅ Metal | ✅ Metal |
| 安装复杂度 | 简单 | 简单 |

## 🎉 总结

这个简化的 LLM 工具提供了与 Ollama 类似的用户体验，但更加轻量级和可定制。通过三个简单的命令，你就可以：

1. **拉取模型**：`./llm pull <model_name>`
2. **列出模型**：`./llm list`
3. **开始聊天**：`./llm run [model_name]`

享受高性能的本地 AI 对话体验！🚀