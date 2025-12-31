import requests
import json

# 测试智谱AI API Key
API_KEY = "82ba3f356586430a8497691d18f86c1c.kKGqtpj9cGKihQWL"

def test_zhipu_api():
    """测试智谱AI API Key是否有效"""

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 测试消息
    messages = [
        {"role": "user", "content": "Hello"}
    ]

    data = {
        "model": "glm-4-flash",
        "messages": messages,
        "temperature": 0.5
    }

    print("开始测试智谱AI API Key...")
    print(f"API Key: {API_KEY[:20]}...{API_KEY[-20:]}")
    print(f"请求URL: {url}")
    print("发送请求...")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        print(f"响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("API Key 有效！")
            try:
                ai_reply = result['choices'][0]['message']['content']
                print(f"AI回复: {ai_reply}")
            except:
                print("获取AI回复失败，但API调用成功")
            return True
        else:
            print("API Key 无效或请求失败")
            print(f"错误详情: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False

if __name__ == "__main__":
    success = test_zhipu_api()
    print("\n" + "="*50)
    if success:
        print("测试通过！API Key 可以使用")
    else:
        print("测试失败！请检查API Key或账户状态")
    print("="*50)
