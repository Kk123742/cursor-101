# Python 基础知识总结

本文档总结了今天学习的两个Python文件中的基础知识。

## 文件1: 101.py

### 代码内容
```python
x = 1
y = 2
print(x+y)
```

### 包含的Python知识点

#### 1. **变量赋值**
- 使用 `=` 运算符进行变量赋值
- Python是动态类型语言，无需声明变量类型
- 变量名遵循标识符命名规则（字母、数字、下划线，不能以数字开头）

#### 2. **整数类型（int）**
- `1` 和 `2` 是整数类型
- Python中的整数可以是任意大小

#### 3. **算术运算**
- `+` 运算符用于加法运算
- 表达式 `x + y` 会先计算，结果为 `3`

#### 4. **内置函数 print()**
- `print()` 是Python的内置函数，用于输出内容到控制台
- 可以打印表达式的结果

### 执行结果
程序输出：`3`

---

## 文件2: glm.py

### 代码内容
```python
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
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]

result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])
```

### 包含的Python知识点

#### 1. **模块导入（import）**
- `import requests` - 导入第三方库requests，用于HTTP请求
- `import json` - 导入标准库json，用于JSON数据处理
- 使用 `import` 关键字导入模块

#### 2. **函数定义（def）**
- 使用 `def` 关键字定义函数
- 函数名：`call_zhipu_api`
- **默认参数**：`model="glm-4-flash"` 是默认参数，调用时可以不传
- 函数可以接收参数并返回值

#### 3. **字符串（str）**
- 字符串用引号（单引号或双引号）包围
- URL、API密钥等都是字符串类型

#### 4. **字典（dict）**
- 使用花括号 `{}` 创建字典
- 键值对格式：`"key": value`
- `headers` 和 `data` 都是字典类型
- 字典用于存储键值对数据

#### 5. **列表（list）**
- 使用方括号 `[]` 创建列表
- `messages` 是一个列表，包含字典元素
- 列表可以存储多个元素

#### 6. **函数调用**
- `requests.post()` - 调用requests库的post方法发送HTTP POST请求
- `response.json()` - 将响应内容解析为JSON格式
- `call_zhipu_api(messages)` - 调用自定义函数

#### 7. **条件语句（if-else）**
- 使用 `if` 进行条件判断
- `response.status_code == 200` 判断HTTP状态码
- `else` 处理其他情况

#### 8. **异常处理（raise）**
- 使用 `raise Exception()` 抛出异常
- 异常信息可以包含错误详情

#### 9. **f-string 格式化字符串**
- 使用 `f"..."` 进行字符串格式化
- 可以在字符串中嵌入变量：`{response.status_code}`

#### 10. **字典访问**
- 使用方括号访问字典值：`result['choices']`
- 可以链式访问嵌套结构：`result['choices'][0]['message']['content']`
- 列表索引从0开始

#### 11. **HTTP请求**
- POST请求用于向服务器发送数据
- 需要设置请求头（headers）和请求体（data）
- 响应对象包含状态码和内容

---

## 知识点对比总结

| 知识点 | 101.py | glm.py |
|--------|--------|--------|
| 变量赋值 | ✅ | ✅ |
| 数据类型 | int | str, dict, list |
| 函数 | 内置函数print() | 自定义函数 + 库函数 |
| 模块导入 | ❌ | ✅ |
| 条件语句 | ❌ | ✅ |
| 异常处理 | ❌ | ✅ |
| 数据结构 | ❌ | dict, list |
| 字符串格式化 | ❌ | ✅ (f-string) |

---

## 学习路径

1. **基础阶段（101.py）**
   - 变量和基本数据类型
   - 简单的算术运算
   - 使用内置函数

2. **进阶阶段（glm.py）**
   - 模块导入和使用
   - 函数定义和调用
   - 复杂数据结构（字典、列表）
   - 条件判断和异常处理
   - 实际应用（API调用）

---

## 下一步学习建议

1. 深入学习Python的数据结构（列表、字典、元组、集合）
2. 学习更多控制流语句（循环、异常处理）
3. 了解面向对象编程（类、对象）
4. 学习文件操作和数据处理
5. 掌握常用标准库和第三方库的使用



