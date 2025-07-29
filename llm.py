#!/usr/bin/env python3
"""
简化的 LLM 命令行工具
支持: llm pull, llm run, llm list
"""

import sys
import argparse
from model_manager import ModelManager

class SimpleLLM:
    def __init__(self):
        self.manager = ModelManager()
    
    def pull(self, model_name):
        """拉取模型"""
        print(f"🚀 正在拉取模型: {model_name}")
        try:
            result = self.manager.pull_model(model_name)
            if result.get('success'):
                print(f"✅ 模型 {model_name} 拉取成功!")
            else:
                print(f"❌ 模型拉取失败: {result.get('error', '未知错误')}")
        except Exception as e:
            print(f"❌ 拉取失败: {str(e)}")
    
    def list_models(self):
        """列出所有模型"""
        print("📋 已下载的模型:")
        try:
            result = self.manager.list_models()
            models = result.get('models', {})
            
            if not models:
                print("  暂无已下载的模型")
                print("  使用 'llm pull <model_name>' 下载模型")
                return
            
            for i, (model_name, model_info) in enumerate(models.items(), 1):
                status = "✅ 已加载" if model_info.get('loaded') else "⭕ 未加载"
                print(f"  {i}. {model_name} - {status}")
                if model_info.get('size'):
                    print(f"     大小: {model_info['size']}")
                if model_info.get('path'):
                    print(f"     路径: {model_info['path']}")
        except Exception as e:
            print(f"❌ 获取模型列表失败: {str(e)}")
    
    def delete(self, model_name):
        """删除模型"""
        print(f"🗑️  正在删除模型: {model_name}")
        
        # 确认删除
        try:
            confirm = input(f"⚠️  确定要删除模型 '{model_name}' 吗？这将删除所有相关文件。(y/N): ").strip().lower()
            if confirm not in ['y', 'yes', '是']:
                print("❌ 取消删除")
                return
            
            result = self.manager.delete_model(model_name)
            if result.get('error'):
                print(f"❌ 删除失败: {result['error']}")
            else:
                print(f"✅ 模型 {model_name} 删除成功!")
                print("💡 提示: 使用 'llm list' 查看剩余模型")
        except KeyboardInterrupt:
            print("\n❌ 取消删除")
        except Exception as e:
            print(f"❌ 删除失败: {str(e)}")
    
    def generate(self, model_name, prompt, max_tokens=100, temperature=0.7):
        """单次文本生成"""
        print(f"🚀 单次生成模式")
        print(f"🤖 模型: {model_name}")
        print(f"📝 提示: {prompt}")
        print("=" * 50)
        
        try:
            # 加载模型
            result = self.manager.load_model(model_name)
            if not result.get('success'):
                print(f"❌ 模型加载失败: {result.get('error')}")
                return
            
            # 生成文本
            response = self.manager.generate_text(
                model_name=model_name,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            if response.get('success'):
                print("🤖 生成结果:")
                print(response['response'])
            else:
                print(f"❌ 生成失败: {response.get('error')}")
                
        except Exception as e:
            print(f"❌ 生成失败: {str(e)}")

    def run(self, model_name=None):
        """运行交互式聊天"""
        if not model_name:
            # 获取第一个可用模型
            result = self.manager.list_models()
            models = result.get('models', {})
            if not models:
                print("❌ 没有可用模型，请先使用 'llm pull <model_name>' 下载模型")
                return
            model_name = list(models.keys())[0]
        
        print(f"🚀 启动模型: {model_name}")
        
        try:
            # 加载模型
            result = self.manager.load_model(model_name)
            if not result.get('success'):
                print(f"❌ 模型加载失败: {result.get('error')}")
                return
            
            print("✅ 模型加载成功!")
            print("💬 开始聊天 (输入 'exit' 退出)")
            print("=" * 50)
            
            # 对话历史
            messages = []
            
            while True:
                try:
                    user_input = input("\n👤 你: ").strip()
                    
                    if user_input.lower() in ['exit', 'quit', 'bye', '退出']:
                        print("👋 再见!")
                        break
                    
                    if not user_input:
                        continue
                    
                    # 添加用户消息
                    messages.append({"role": "user", "content": user_input})
                    
                    # 保持对话历史在合理长度
                    if len(messages) > 10:
                        messages = messages[-8:]
                    
                    print("🤖 AI: ", end="", flush=True)
                    
                    # 流式生成回复
                    full_reply = ""
                    try:
                        for chunk in self.manager.chat_completion_stream(model_name, messages):
                            if not chunk.get('success'):
                                print(f"❌ 生成失败: {chunk.get('error')}")
                                break
                            
                            content = chunk.get('content', '')
                            if content:
                                print(content, end="", flush=True)
                                full_reply += content
                            
                            # 检查是否完成
                            if chunk.get('done'):
                                full_reply = chunk.get('full_response', full_reply)
                                break
                        
                        print()  # 换行
                        
                        if full_reply:
                            # 添加AI回复到历史
                            messages.append({"role": "assistant", "content": full_reply})
                        
                    except Exception as e:
                        print(f"\n❌ 流式生成错误: {str(e)}")
                        # 回退到非流式模式
                        response = self.manager.chat_completion(model_name, messages)
                        if response.get('success'):
                            reply = response['response']
                            print(reply)
                            messages.append({"role": "assistant", "content": reply})
                        else:
                            print(f"❌ 生成失败: {response.get('error')}")
                
                except KeyboardInterrupt:
                    print("\n👋 再见!")
                    break
                except Exception as e:
                    print(f"\n❌ 错误: {str(e)}")
        
        except Exception as e:
            print(f"❌ 运行失败: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="简化的 LLM 命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  llm pull microsoft/Phi-3-mini-4k-instruct-gguf    # 拉取模型
  llm list                                           # 列出模型
  llm delete <model_name>                            # 删除模型
  llm run                                           # 运行第一个可用模型
  llm run Qwen/Qwen2-1.5B-Instruct-GGUF            # 运行指定模型
  llm generate <model> "你好"                        # 单次生成文本
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # pull 命令
    pull_parser = subparsers.add_parser('pull', help='拉取模型')
    pull_parser.add_argument('model', help='模型名称 (例: microsoft/Phi-3-mini-4k-instruct-gguf)')
    
    # list 命令
    subparsers.add_parser('list', help='列出已下载的模型')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除模型')
    delete_parser.add_argument('model', help='要删除的模型名称')
    
    # run 命令
    run_parser = subparsers.add_parser('run', help='运行交互式聊天')
    run_parser.add_argument('model', nargs='?', help='模型名称 (可选，默认使用第一个可用模型)')
    
    # generate 命令
    generate_parser = subparsers.add_parser('generate', help='单次文本生成')
    generate_parser.add_argument('model', help='模型名称')
    generate_parser.add_argument('prompt', help='输入提示文本')
    generate_parser.add_argument('--max-tokens', type=int, default=32768, help='最大生成token数 (默认: 32768)')
    generate_parser.add_argument('--temperature', type=float, default=0.7, help='温度参数 (默认: 0.7)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    llm = SimpleLLM()
    
    if args.command == 'pull':
        llm.pull(args.model)
    elif args.command == 'list':
        llm.list_models()
    elif args.command == 'delete':
        llm.delete(args.model)
    elif args.command == 'run':
        llm.run(args.model)
    elif args.command == 'generate':
        llm.generate(args.model, args.prompt, args.max_tokens, args.temperature)

if __name__ == "__main__":
    main()