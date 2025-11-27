import requests
import json

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "22facac2bdb24611842f3aae2c496c2a.cOPfGBcqirfOOkGr",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
# 多轮对话循环，直到用户输入 '再见' 结束
while True:  # 表示“当条件为真时一直循环”。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话：")
    role_system = "你是一个哲学家，如果你判断用户已经不想继续交流，只回复：再见"
    messages = [
        {"role": "user", "content": role_system},{"role": "user", "content": user_input}
    ]
    result = call_zhipu_api(messages)
    reply = (result['choices'][0]['message']['content'])
    print(reply)

    if reply =="再见":
     print("对话结束。")
     break