"""
时间 MCP 示例
展示如何使用 MCP（Model Context Protocol）让 AI 获取时间

前置要求：
pip install mcp-server-time
"""

import subprocess
import json
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.json")

def load_memory():
    """从 JSON 文件加载对话记忆"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保有 conversations 键
                if "conversations" not in data:
                    data["conversations"] = []
                return data
        except:
            return {"conversations": []}
    return {"conversations": []}

def save_memory(memory):
    """保存对话记忆到 JSON 文件（不包含时间信息）"""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

class TimeMCP:
    """MCP 客户端"""
    
    def __init__(self):
        self.process = None
        self.request_id = 1
        self.initialized = False
        
    def start_server(self):
        """启动 MCP 服务器"""
        try:
            self.process = subprocess.Popen(
                ["python", "-m", "mcp_server_time"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            time.sleep(1)
            return self._initialize()
        except FileNotFoundError:
            print("❌ 请先安装: pip install mcp-server-time")
            return False
    
    def _read_response(self, timeout=5):
        """读取 JSON-RPC 响应"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            line = self.process.stdout.readline()
            if line:
                try:
                    return json.loads(line.strip())
                except:
                    continue
            time.sleep(0.1)
        return None
    
    def _initialize(self):
        """MCP 初始化流程"""
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "time-client", "version": "1.0.0"}
            }
        }
        self.request_id += 1
        
        self.process.stdin.write(json.dumps(init_request) + "\n")
        self.process.stdin.flush()
        
        response = self._read_response()
        if response and "result" in response:
            notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}
            self.process.stdin.write(json.dumps(notification) + "\n")
            self.process.stdin.flush()
            self.initialized = True
            return True
        return False
    
    def get_time(self, timezone=None):
        """调用 MCP 工具获取时间"""
        if not self.initialized:
            return None
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "get_current_time",
                "arguments": {"timezone": timezone} if timezone else {}
            }
        }
        self.request_id += 1
        
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        response = self._read_response()
        if response:
            if "result" in response:
                result = response["result"]
                if "content" in result and len(result["content"]) > 0:
                    text = result["content"][0].get("text", "")
                    try:
                        return json.loads(text)
                    except:
                        return text
            elif "error" in response:
                return {"error": response["error"]}
        return None
    
    def close(self):
        if self.process:
            self.process.terminate()

def main():
    """Chatbot 集成示例"""
    import requests
    
    try:
        from config import ZHIPU_API_KEY
    except ImportError:
        ZHIPU_API_KEY = "你的智谱AI_API_KEY"
    
    def call_api(messages):
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {"Authorization": ZHIPU_API_KEY, "Content-Type": "application/json"}
        data = {"model": "glm-4-flash", "messages": messages, "temperature": 0.5}
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.status_code == 200 else None
    
    mcp = TimeMCP()
    if not mcp.start_server():
        return
    
    print("=" * 50)
    print("MCP 示例")
    print("=" * 50)
    
    memory = load_memory()
    
    try:
        while True:
            user_input = input("\n你: ").strip()
            if not user_input or user_input.lower() in ['退出', 'exit']:
                break
            
            messages = [{"role": "user", "content": user_input}]
            
            # 每次对话都调用 MCP 获取当前时间（用于当前对话）
            current_time_info = mcp.get_time()
            current_datetime = ""
            if current_time_info and isinstance(current_time_info, dict) and "error" not in current_time_info:
                current_datetime = current_time_info.get('datetime', '')
            
            # 检测时间问题并调用 MCP
            time_keywords = ["时间", "几点", "时区", "几几年", "几月", "几号", "几点钟", "什么时候"]
            is_time_question = any(kw in user_input for kw in time_keywords)
            
            if is_time_question:
                timezone = None
                if "上海" in user_input or "中国" in user_input or "杭州" in user_input:
                    timezone = "Asia/Shanghai"
                elif "纽约" in user_input:
                    timezone = "America/New_York"
                elif "东京" in user_input or "日本" in user_input:
                    timezone = "Asia/Tokyo"
                
                # 调用 MCP 获取最新时间
                time_info = mcp.get_time(timezone)
                
                if time_info and isinstance(time_info, dict) and "error" not in time_info:
                    datetime_str = time_info.get('datetime', '')
                    timezone_str = time_info.get('timezone', '')
                    messages.insert(0, {
                        "role": "system",
                        "content": f"当前时间信息：{datetime_str}，时区：{timezone_str}。请基于这个准确的时间信息回答用户的问题。"
                    })
                else:
                    messages.insert(0, {
                        "role": "system",
                        "content": "时间工具调用失败，无法获取实时时间信息。"
                    })
            
            # 调用 AI
            result = call_api(messages)
            if result:
                ai_response = result['choices'][0]['message']['content']
                print(f"AI: {ai_response}")
                
                # 保存对话到记忆（去掉时间信息，避免混淆）
                conversation = {
                    "user": user_input,
                    "assistant": ai_response
                }
                memory["conversations"].append(conversation)
                save_memory(memory)
            
    except KeyboardInterrupt:
        pass
    finally:
        mcp.close()

if __name__ == "__main__":
    main()