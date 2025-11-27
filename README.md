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

---

## 文件3: 302_glm_catch a mole.py（打地鼠游戏）

### 代码功能
实现一个"谁是卧底"游戏，AI随机扮演不同角色，用户通过提问猜测AI的身份。

### 包含的Python知识点

#### 1. **random模块 - 随机选择**
- `import random` - 导入随机数模块
- `random.choice(role_system)` - 从列表中随机选择一个元素
- 用于游戏开始时随机分配角色
- 示例：`current_role = random.choice(["A", "B", "C"])`

#### 2. **多行字符串（三引号字符串）**
- 使用三个引号 `"""` 或 `'''` 创建多行字符串
- 可以保留字符串中的换行和格式
- 用于定义复杂的系统提示词（game_system）
- 适合存储长文本内容

#### 3. **f-string 格式化字符串（进阶）**
- `f"""...{variable}..."""` - 在多行字符串中使用变量
- `{current_role}` - 在字符串中嵌入变量值
- 动态生成包含变量的长文本
- 示例：`game_system = f"""你的身份是：{current_role}"""`

#### 4. **列表的append()方法**
- `conversation_history.append({...})` - 向列表末尾添加元素
- 用于维护对话历史，每次对话后添加用户消息和AI回复
- 列表是可变对象，append()会修改原列表

#### 5. **字典的嵌套结构**
- 列表中可以包含字典：`[{"role": "system", "content": "..."}]`
- 字典的键值对：`{"role": "user", "content": user_input}`
- 构建符合API要求的消息格式
- 展示复杂数据结构的组合使用

#### 6. **字符串的in操作符**
- `"再见" in assistant_reply` - 检查字符串是否包含子字符串
- 返回布尔值（True/False）
- 用于判断游戏是否结束（AI回复中包含"再见"）

#### 7. **从其他模块导入函数**
- `from xunfei_tts import text_to_speech` - 从自定义模块导入函数
- 使用其他文件中定义的函数（文本转语音功能）
- 展示模块化编程的思想

#### 8. **系统角色（system role）**
- `{"role": "system", "content": game_system}` - 设置AI的系统提示
- 用于定义AI的角色、规则和行为模式
- 系统消息在对话开始时设置，影响整个对话过程

#### 9. **对话历史维护**
- 使用列表 `conversation_history` 存储所有对话
- 每次API调用时传入完整历史，让AI记住之前的对话
- 实现多轮对话的上下文连续性
- 关键：每次对话后都要将用户输入和AI回复添加到历史中

---

## 文件4: 303_glm_game.py（附身危机游戏）

### 代码功能
实现一个更复杂的推理游戏"附身危机"，玩家需要通过提问找出被附身的角色。

### 包含的Python知识点

#### 1. **复杂系统提示词设计**
- 使用多行字符串定义详细的游戏规则
- 包含游戏背景、角色设定、规则说明等
- 展示如何通过提示词工程控制AI行为
- 提示词的质量直接影响AI的表现

#### 2. **对话历史管理（进阶）**
- 初始化时添加系统消息：`[{"role": "system", "content": game_system}]`
- 每次用户输入后追加到历史：`conversation_history.append(...)`
- 每次AI回复后也追加到历史，保持完整对话链
- 确保AI能够记住所有之前的对话内容

#### 3. **while True 无限循环**
- `while True:` - 创建无限循环
- 使用 `break` 语句退出循环
- 配合条件判断实现游戏结束逻辑
- 适合需要持续交互的程序

#### 4. **字符串包含判断**
- `if "再见" in assistant_reply:` - 检查回复中是否包含特定关键词
- 用于判断游戏是否结束
- 简单但有效的条件判断方式

#### 5. **变量作用域**
- `current_role` 在循环外部定义，循环内部可以访问
- 展示变量的作用域概念
- 全局变量可以在函数和循环中使用

---

## 文件5: 401_memory.py（记忆系统）

### 代码功能
实现对话历史的持久化存储，程序重启后可以恢复之前的对话。

### 包含的Python知识点

#### 1. **os模块 - 文件操作**
- `import os` - 导入操作系统接口模块
- `os.path.exists(MEMORY_FILE)` - 检查文件是否存在
- 返回布尔值（True/False）
- 在读写文件前先检查文件是否存在，避免错误

#### 2. **JSON文件读写**
- **读取JSON**：`json.load(f)` - 从文件对象读取JSON数据并解析为Python对象
- **写入JSON**：`json.dump(data, f, ...)` - 将Python对象写入JSON文件
- `ensure_ascii=False` - 保存中文时不转义为Unicode，直接保存中文
- `indent=2` - 格式化输出，每个层级缩进2个空格，让文件更易读
- JSON是存储结构化数据的常用格式

#### 3. **with语句（上下文管理器）**
- `with open(file, 'r', encoding='utf-8') as f:` - 自动管理文件资源
- 文件使用完毕后自动关闭，无需手动调用 `f.close()`
- 即使发生异常也能正确关闭文件
- `encoding='utf-8'` - 指定文件编码，确保中文正确读写
- 这是Python推荐的文件操作方式

#### 4. **异常处理（try-except）**
- `try: ... except Exception as e:` - 捕获和处理异常
- `except KeyboardInterrupt:` - 捕获用户中断（Ctrl+C）
- `except Exception as e:` - 捕获所有其他异常
- 确保程序异常退出时也能保存数据
- 提高程序的健壮性

#### 5. **字典的get()方法**
- `data.get('history', [])` - 安全获取字典值
- 如果键存在，返回对应的值
- 如果键不存在，返回默认值（这里是空列表 `[]`）
- 避免 `KeyError` 异常
- 比直接访问 `data['history']` 更安全

#### 6. **列表切片（slicing）**
- `conversation_history[1:]` - 从索引1开始到末尾的所有元素
- `[1:]` 表示跳过第一个元素（索引0）
- 用于在保留完整历史的同时，避免重复系统提示
- 列表切片返回新列表，不修改原列表

#### 7. **列表拼接（+操作符）**
- `[A] + [B, C]` - 将两个列表合并成一个新列表
- `[{"role": "system", ...}] + conversation_history[1:]` - 组合系统消息和历史记录
- 创建新的列表，不修改原列表
- 用于构建API调用所需的消息格式

#### 8. **字符串方法**
- `strip()` - 去除字符串首尾空白字符
- `replace(old, new)` - 替换字符串中的字符
- 可以链式调用：`reply.strip().replace(" ", "")`
- 用于清理和格式化字符串

#### 9. **datetime模块**
- `from datetime import datetime` - 导入日期时间模块
- `datetime.now()` - 获取当前时间
- `strftime("%Y-%m-%d %H:%M:%S")` - 格式化时间为字符串
- 用于记录最后更新时间
- 时间格式：年-月-日 时:分:秒

#### 10. **函数定义和调用**
- `load_memory()` - 加载记忆的函数，返回对话历史列表
- `save_memory(conversation_history, role_system)` - 保存记忆的函数
- 函数封装了文件操作的逻辑，提高代码复用性
- 函数可以没有返回值（返回None）

#### 11. **布尔值判断**
- `if not conversation_history:` - 判断列表是否为空
- 空列表的布尔值为 `False`，`not False` 为 `True`
- 用于判断是否是第一次运行程序
- Python中空容器（列表、字典等）的布尔值都是False

#### 12. **常量定义**
- `MEMORY_FILE = "conversation_memory.json"` - 定义常量
- 使用大写字母命名常量（Python约定）
- 便于统一管理和修改
- 避免在代码中硬编码字符串

---

## 文件6: 402_memory clonebot.py（克隆机器人记忆系统）

### 代码功能
实现基于外部记忆文件的角色克隆系统，从JSON文件加载角色的说话风格和记忆。

### 包含的Python知识点

#### 1. **os.path.join() - 路径拼接**
- `os.path.join(MEMORY_FOLDER, memory_file)` - 跨平台路径拼接
- 自动处理不同操作系统的路径分隔符（Windows用`\`，Linux/Mac用`/`）
- 比字符串拼接更安全可靠
- 示例：`os.path.join("folder", "file.json")` → `"folder/file.json"` 或 `"folder\file.json"`

#### 2. **isinstance() - 类型检查**
- `isinstance(data, list)` - 检查对象是否为指定类型
- `isinstance(data, dict)` - 检查对象是否为字典类型
- 返回布尔值（True/False）
- 用于判断JSON数据的格式（数组或字典）
- 比使用 `type()` 更推荐

#### 3. **列表推导式（List Comprehension）**
- `[item.get('content', '') for item in data if ...]` - 简洁的列表生成方式
- 等价于for循环，但更简洁优雅
- 用于从复杂数据结构中提取数据
- 可以包含条件判断：`[x for x in list if condition]`

#### 4. **条件表达式（三元表达式）**
- `len(data) if isinstance(data, list) else 1` - 根据条件返回不同值
- 语法：`value_if_true if condition else value_if_false`
- 简洁的条件判断语法
- 适合简单的条件赋值

#### 5. **字符串的join()方法**
- `'\n'.join(contents)` - 用指定分隔符连接字符串列表
- 将列表中的多个字符串用换行符连接成一个字符串
- 比循环拼接字符串更高效
- 示例：`'\n'.join(['a', 'b', 'c'])` → `"a\nb\nc"`

#### 6. **字符串的strip()方法**
- `memory_content.strip()` - 去除首尾空白字符
- 用于检查字符串是否为空（去除空白后）
- 返回新字符串，不修改原字符串

#### 7. **字典的get()方法（进阶）**
- `item.get('content', '')` - 安全获取嵌套字典的值
- 在列表推导式中使用，避免KeyError
- 如果键不存在，返回默认值（空字符串）

#### 8. **多行字符串拼接**
- `"\n\n".join(role_prompt_parts)` - 用双换行符连接多个字符串
- 构建结构化的提示词
- 用于组合多个文本片段

#### 9. **函数返回值处理**
- 函数可以返回字符串
- `role_system = roles("zjy")` - 接收函数返回值并赋值给变量
- 函数可以返回任何类型的值

#### 10. **字典映射（ROLE_MEMORY_MAP）**
- 使用字典建立角色名到文件名的映射关系
- `ROLE_MEMORY_MAP.get(role_name)` - 根据角色名获取对应的文件名
- 便于管理和扩展多个角色
- 展示字典作为映射表的用法

#### 11. **嵌套字典结构**
- `role_personality` 是一个字典，值是字符串
- 展示如何用字典组织多个角色的设定
- 字典可以存储任何类型的值

#### 12. **空列表初始化**
- `conversation_history = [{"role": "system", "content": system_message}]` - 初始化时包含系统消息
- 与401.py不同，这里不保存对话历史到文件
- 展示不同的初始化方式

#### 13. **ASCII艺术**
- 使用多行字符串存储ASCII字符画
- 展示字符串的另一种应用场景
- 可以用于美化程序输出

---

## 知识点进阶对比

| 知识点 | 302/303 | 401 | 402 |
|--------|---------|-----|-----|
| 文件操作 | ❌ | ✅ | ✅ |
| JSON读写 | ❌ | ✅ | ✅ |
| 异常处理 | ❌ | ✅ | ❌ |
| 类型检查 | ❌ | ❌ | ✅ |
| 列表推导式 | ❌ | ❌ | ✅ |
| 路径操作 | ❌ | ❌ | ✅ |
| 对话持久化 | ❌ | ✅ | ❌ |
| 外部记忆加载 | ❌ | ❌ | ✅ |
| 随机数生成 | ✅ | ❌ | ❌ |
| 多行字符串 | ✅ | ✅ | ✅ |

---

## 综合学习路径

1. **基础阶段（101.py, glm.py）**
   - 变量、数据类型、函数
   - 模块导入、API调用
   - 基本控制流

2. **游戏开发阶段（302, 303）**
   - 随机数生成
   - 多行字符串
   - 对话历史维护
   - 循环控制
   - 字符串操作

3. **数据持久化阶段（401）**
   - 文件读写
   - JSON处理
   - 异常处理
   - 上下文管理器（with语句）
   - 列表切片和拼接

4. **高级应用阶段（402）**
   - 路径操作
   - 类型检查
   - 列表推导式
   - 复杂数据处理
   - 模块化设计

---

## 核心概念总结

### 1. **对话历史管理**
- **内存中维护**：使用列表存储对话，程序运行期间有效
- **持久化存储**：使用JSON文件保存，程序重启后恢复
- **系统消息**：使用 `{"role": "system"}` 设置AI行为
- **消息格式**：`{"role": "user/assistant/system", "content": "..."}`

### 2. **文件操作模式**
- `'r'` - 只读模式
- `'w'` - 写入模式（覆盖原有内容）
- `encoding='utf-8'` - 指定编码，支持中文
- 使用 `with` 语句确保文件正确关闭

### 3. **异常处理策略**
- 文件操作必须使用 try-except
- 区分不同类型的异常（KeyboardInterrupt vs Exception）
- 确保异常时也能保存重要数据
- 提供友好的错误提示

### 4. **代码组织原则**
- 使用函数封装重复逻辑
- 使用常量定义配置
- 使用字典映射管理多个选项
- 模块化设计，提高代码复用性

### 5. **数据结构选择**
- **列表**：用于存储有序的对话历史
- **字典**：用于存储键值对（配置、映射关系）
- **嵌套结构**：列表包含字典，字典值可以是列表
- 根据数据特点选择合适的数据结构
