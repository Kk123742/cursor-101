import requests

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    """
    调用智谱API获取AI回复
    
    参数：
        messages: 对话消息列表，格式：[{"role": "user", "content": "..."}]
        model: 模型名称，默认为 "glm-4-flash"
    
    返回：
        API返回的JSON数据（字典格式）
    """
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "82ba3f356586430a8497691d18f86c1c.kKGqtpj9cGKihQWL",
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
