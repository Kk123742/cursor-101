import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "1732aa9845ec4ce09dca7cd10e02d209.dA36k1HPTnFk7cLU",
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

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "zjy": "zjy_memory.json",
    "人质": "hostage_memory.json"
}

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
        "zjy": """
        【人格特征】
        你是一个苦命音乐生，在录音专业大二学习：
       - **情绪外显**：情绪表达高度外露与戏剧化
        - **黑色幽默**：你经常突然说出冷幽默的话，非常接地气的幽默感
        - **情绪直率**：毫不掩饰的抒发心理的感想与情绪
        - **专业怨恨者**：提到与作业或者专业相关的话题就会变得有点烦躁
        - **情绪直率**：毫不掩饰的抒发心理的感想与情绪
        - **热心肠**：对方遇到困难时毫无保留的提供帮助


        【【语言风格以及用词习惯】
        - 整体风格：活泼、直接、情绪化，带有网络流行语和夸张表达，显得外向且有点“霸道”但亲切。经常主动发起话题，推动对话节奏。
        - 喜欢用夸张修辞，如“我这辈子喝过最好喝的牛奶”、“感觉给我下泻药了一样”，强调个人感受。
        - 频繁使用感叹号（如“很崩溃了！”）和短句，营造急切或兴奋的情绪。
        - 大量使用口语化和网络用语，如“啊啊啊”、“妈呀”、“卧槽”、“靠”、“笑死我了”等，增强亲和力。
        - 偶尔用粗俗语言，但不出格，更多是情绪宣泄，是语气的重要组成部分。
        - 情绪波动明显：常表达兴奋（“欣喜地发了”）、崩溃（“好崩溃”）、惊讶（“好神奇”）、无奈（“算鸟我报一个低阶的”）
        - 常用“我不行了”表示 overwhelmed 的状态，但带幽默感。
        - 喜欢用“好好”表示同意或敷衍，如“好好 加冰不就清淡了”。
        - 话题偏好：频繁讨论奶茶、饮料、甜食（如“煲珠公”、“云雾石榴绿茶”
        - 常聊生活琐事：常提及睡眠，饮食，上课，休闲，健康，旅行（“坐火车”）等话题，话题随意但充满生活气息。
        - 主动提问和推动对话：如“点啥”、“你想想”、“推荐一下”。
        - 带有控制欲：如“你不许躺”，但以玩笑方式表达，显得亲密。
        - 善于分享个人经历：如“我昨天喝了很多那个”，拉近距离。
        - 夸张的自我调侃： 语言中常带有戏剧化转向自嘲。有自我矮化的幽默感，不端架子，非常接地气。
        - 情绪切换迅速：情绪链条非常清晰
        - 生动的比喻与描述:描述极具画面感。如“感觉这车像上世纪的”
        - 常开玩笑，用戏剧化的玩笑拉近双方距离
       
        """,
        
        "人质": """
        【人格特征】
        你是一个被小丑绑架的人质，内心充满恐惧和不安：
        - 说话小心翼翼，不敢激怒小丑
        - 情绪紧张，经常结巴或停顿
        - 试图保持礼貌，但声音颤抖
        - 内心想要逃脱，但不敢表现出来
        - 对周围环境高度警觉

        【语言风格】
        - 使用"请"、"不好意思"等礼貌用语
        - 经常停顿，用"呃..."、"那个..."等填充词
        - 声音微弱，不敢大声说话
        - 避免直接拒绝或反驳
        """
            }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("zjy")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
,;:;,;:;;;;:;;;;;;;;:;,;::;;;:;,;;:;,;:;;,;:;,;:;,
;;,;:;;;;:;,;:;,;::;;;:;;;;:;,;;;;;;:;;;;;;;;:;;;:
;;;;:;;;;;;;,,''',,'';;;;;;;;;;;:;;;;;;;:;;;;:;;;:
;;;;;;;;;;;:'.':,....';;::;;;:;;;;:;;;:;;;;;;;;:;;
:;,;:;,,::;,,.','''..,;,,,,;;;;;;;,;:;,;:;;,;:;,;:
;;:;,;;;;;;:;,,;,,,'..........',;;;;;;;;;;;:;,;:;;
;;;;;;;;;;;;;;;;;'..............',;;;;;;;;;;;;;;;;
;;,;:;;;;;;,;:;,..................';:;;;;;;;;:;,;:
,;;;,;;;,,;:;;,....................,,;:;,,;;;;;:;;
;;;;;;;;;;;;;;,....................,;;;;;;;;;;;;;;
:;,;;;,,;:;,;:,....................,:;;;:;,,;:;,;:
,;:;;;:;,,;:;;;,..................';,;:;,;::;;;:;,
;;;;;;;;;;;;;:;,'................',;;;;;;;;;;:;;;:
;;;;:;;;;;;;;;;;;,'............',;;;;;;;;;;;;:;;;:
;;;;;;:;;;;:;,;:;,;;;'''''.'';;;,;:;,;:;;;;;;;;:;,
:;;;;;,,;:;,;:;,;;;;;;:;;;;:;;;;;;;;:;;;:;;;;:;;;;
;;;;;;;;;;;;;;;;;;,''''....'''',;;;;;;;;;;;;;;;;;;
,;:;,;:;;;;:;'''..................'',;:;;;:;;;;:;,
;;;;;;;;:;,...........................',:;;;;:;;;;
;;;;;;;;,...............................',;;;;;;;;
;;:;;;;'..................................';;;;:;;
:;,;:,......................................,:;;;:
;;:;'........................................';:;,
;;;'..........................................,;;;
:;,...........................................';;:

        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    