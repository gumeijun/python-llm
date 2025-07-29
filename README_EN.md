# Python LLM - Local Large Language Model Service

English Version | [中文版](./README.md)

A lightweight local large language model service, similar to Ollama, supporting GGUF format model pulling, management, and inference.

## 🌟 Features

- **🚀 Quick Deployment**: One-click startup with no complex configuration
- **📦 GGUF Support**: Native support for quantized GGUF format models
- **🎯 Multi-Interface**: Support for API, CLI, and web interface
- **⚡ Hardware Acceleration**: Auto-detect and use Metal (macOS) or CUDA (Linux/Windows)
- **🔄 Streaming Response**: Support for streaming text generation
- **💾 Memory Optimization**: Intelligent model loading and memory management

## 🚀 Quick Start

### Install Dependencies

```bash
# Clone project
git clone <repository-url>
cd python-llm

# Install dependencies
pip install -r requirements.txt
```

### Start Service

```bash
# Start API service
python main.py

# Or use startup script
./start.sh
```

Service will start at http://localhost:8000, visit /docs for API documentation.

### Command Line Usage

```bash
# Pull model
./llm pull microsoft/Phi-3-mini-4k-instruct-gguf

# List models
./llm list

# Run interactive chat
./llm run microsoft/Phi-3-mini-4k-instruct-gguf

# Single text generation
./llm generate microsoft/Phi-3-mini-4k-instruct-gguf "Hello, please introduce machine learning"
```

## 📖 Detailed Usage

### API Endpoints

#### 1. Pull Model
```bash
curl -X POST "http://localhost:8000/models/pull" \
     -H "Content-Type: application/json" \
     -d '{"model_name": "microsoft/Phi-3-mini-4k-instruct-gguf"}'
```

#### 2. Text Generation
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "model_name": "microsoft/Phi-3-mini-4k-instruct-gguf",
       "prompt": "Hello",
       "max_tokens": 512,
       "temperature": 0.7
     }'
```

#### 3. Chat Completion
```bash
curl -X POST "http://localhost:8000/generate/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "model_name": "microsoft/Phi-3-mini-4k-instruct-gguf",
       "messages": [
         {"role": "user", "content": "Hello"}
       ],
       "max_tokens": 512
     }'
```

### Recommended Models

| Model Name | Size | Use Case |
|------------|------|----------|
| `microsoft/Phi-3-mini-4k-instruct-gguf` | 2.4GB | General conversation |
| `Qwen/Qwen2-1.5B-Instruct-GGUF` | 3.2GB | Chinese conversation |
| `unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF` | 1.5GB | Lightweight inference |
| `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF` | 8GB | High-quality inference |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 0.0.0.0 | Service listening address |
| `PORT` | 8000 | Service port |
| `USE_GPU` | True | Whether to use GPU acceleration |
| `LOG_LEVEL` | INFO | Log level |

## 🏗️ Project Structure

```
python-llm/
├── main.py              # Main program entry
├── model_manager.py     # Model manager
├── inference.py         # Inference engine
├── config.py           # Configuration file
├── llm.py              # Command line tool
├── llm                 # Command line entry script
├── api/                # API module
│   ├── __init__.py
│   ├── models.py       # Model management API
│   └── generate.py     # Text generation API
├── utils/              # Utility module
│   ├── __init__.py
│   └── download.py     # Model downloader
├── models/             # Model storage directory
│   └── models_info.json # Model information file
└── requirements.txt    # Dependencies list
```

## 🔧 Development Guide

### Adding New Features

1. **Add new API endpoints**: Create new route files in the `api/` directory
2. **Extend model support**: Modify model selection logic in `utils/download.py`
3. **Custom configuration**: Add new configuration items in `config.py`

### Debug Mode

```bash
# Enable debug mode
export DEBUG=true
python main.py

# View detailed logs
export LOG_LEVEL=DEBUG
python main.py
```

## 🐛 Common Issues

### Model Download Failure
- **Check network**: Ensure access to huggingface.co
- **Proxy settings**: Set HTTP_PROXY/HTTPS_PROXY environment variables
- **Retry**: Delete corresponding folder in models directory and retry

### Insufficient Memory
- **Use smaller models**: Choose 1.5B or smaller models
- **Quantized models**: Use Q4_0 or Q8_0 quantized versions
- **Disable GPU**: Set USE_GPU=false to use CPU

### Slow Inference Speed
- **Check device**: Check logs to confirm GPU acceleration is being used
- **Model caching**: First load is slower, subsequent loads will be cached
- **Adjust parameters**: Reduce max_tokens or use faster sampling parameters

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

## 📞 Support

For help, please use the following methods:
1. Check project documentation
2. Run test scripts
3. Submit GitHub Issue