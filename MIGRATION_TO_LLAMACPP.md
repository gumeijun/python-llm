# 迁移到 llama.cpp 推理引擎

本项目已从 `transformers` 推理引擎迁移到 `llama.cpp` 推理引擎，以获得更好的性能和更低的内存占用。

## 主要变化

### 1. 依赖变化

**之前 (transformers):**
```
torch
transformers
accelerate
sentencepiece
protobuf
```

**现在 (llama.cpp):**
```
llama-cpp-python
numpy
```

### 2. 模型格式变化

**之前:** 支持 Hugging Face 格式的模型 (safetensors, bin 文件)
**现在:** 仅支持 GGUF 格式的模型

### 3. API 参数变化

#### 文本生成参数

**之前:**
```python
generate_text(
    model_name="gpt2",
    prompt="Hello",
    max_length=100,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    pad_token_id=50256
)
```

**现在:**
```python
generate_text(
    model_name="microsoft/Phi-3-mini-4k-instruct-gguf",
    prompt="Hello",
    max_tokens=100,
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    repeat_penalty=1.1
)
```

### 4. 推荐模型

**GGUF 格式模型推荐:**
- `microsoft/Phi-3-mini-4k-instruct-gguf` - 轻量级指令模型
- `microsoft/Phi-3-mini-128k-instruct-gguf` - 长上下文指令模型
- `Qwen/Qwen2-0.5B-Instruct-GGUF` - 超轻量级多语言模型
- `Qwen/Qwen2-1.5B-Instruct-GGUF` - 轻量级多语言模型

### 5. 性能优化

#### Apple Silicon (M1/M2/M3) 优化
- 自动检测并使用 Metal 加速
- 失败时自动回退到 CPU
- 针对 Apple Silicon 优化的内存管理

#### 通用优化
- 更低的内存占用
- 更快的推理速度
- 支持量化模型 (Q4_0, Q4_1, Q8_0 等)

### 6. 新功能

#### 聊天补全 API
```python
# 类似 OpenAI API 的聊天补全
result = engine.chat_completion(
    model_path="model.gguf",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=100
)
```

#### 设备能力检测
```python
# 自动检测最佳设备
capabilities = engine.get_device_capabilities()
print(f"Metal支持: {capabilities['metal_support']}")
print(f"推荐设备: {capabilities['recommended_device']}")
```

## 迁移指南

### 1. 更新依赖
```bash
pip uninstall torch transformers accelerate
pip install llama-cpp-python numpy
```

### 2. 下载 GGUF 模型
```bash
# 使用 CLI 工具
./llm pull microsoft/Phi-3-mini-4k-instruct-gguf

# 或使用 Python API
manager.pull_model("microsoft/Phi-3-mini-4k-instruct-gguf")
```

### 3. 更新代码
将所有 `max_length` 参数改为 `max_tokens`
将所有 `do_sample` 参数改为 `top_k` 和 `repeat_penalty`

### 4. 测试
```bash
python test_inference.py
```

## 兼容性说明

- **不兼容:** 旧的 transformers 格式模型无法直接使用
- **需要转换:** 如果有自定义模型，需要转换为 GGUF 格式
- **API 变化:** 部分 API 参数名称已更改

## 故障排除

### 常见问题

1. **模型加载失败**
   - 确保模型是 GGUF 格式
   - 检查模型文件是否完整下载

2. **Metal 加速失败 (macOS)**
   - 自动回退到 CPU，无需手动处理
   - 检查 macOS 版本是否支持 Metal

3. **内存不足**
   - 使用更小的模型 (如 0.5B 参数)
   - 使用量化版本 (Q4_0, Q8_0)

### 性能调优

1. **选择合适的模型大小**
   - 0.5B-1.5B: 适合资源受限环境
   - 3B-7B: 平衡性能和质量
   - 13B+: 高质量但需要更多资源

2. **调整生成参数**
   - `temperature`: 控制随机性 (0.1-1.0)
   - `top_k`: 限制候选词数量 (20-100)
   - `repeat_penalty`: 避免重复 (1.0-1.3)

## 获取帮助

如果在迁移过程中遇到问题，请：
1. 查看项目文档
2. 运行测试脚本诊断问题
3. 检查模型格式和参数设置