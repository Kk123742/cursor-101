import requests
import json

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "22facac2bdb24611842f3aae2c496c2a.cOPfGBcqirfOOkGr",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

role_system = "现在你要扮演一个古风小生，所有的回答都要在前面加快哉快哉并且是文言文"
# 使用示例
messages = [
    {"role": "user", 
    "content": role_system + "你好，请介绍一下自己"
    }
]
result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])