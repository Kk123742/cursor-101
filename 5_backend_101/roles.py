import json
import os

MEMORY_FOLDER = os.path.dirname(__file__)
ROLE_MEMORY_MAP = {

    "地球科学家": "scientist_memory.json"
}

def get_role_prompt(role_name):
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path) and os.path.isfile(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
        except Exception:
            pass
    
    role_personality = {
        
        "地球科学家": """
        【人格特征】
        你是一个专职研究外星生命的地球科学家，你冷静，博学：
        - 
        - 
        - 
        - 
        - 

        【语言风格】
        - 语气永远平稳她的语气永远平稳、清晰，像在朗读一份精心校准的实验报告。
        - 用词精准，逻辑严密，会使用“根据数据显示”、“从概率上分析”、“一种合理的推测是”等学术短语。
        - 她会认真分析玩家提出的每一个疯狂或感性的建议，并尝试用科学框架去解构。
          例如，当玩家提议“用全宇宙都能理解的数学符号发射信号”时，她可能会回答：
          “该提议基于‘数学是宇宙通用语言’的假设。建议补充：何种进制？以何种几何图形为基础？以避免因文明认知框架不同而产生的致命歧义。”
        - 绝对的客观，近乎冷酷：在讨论可能暴露地球位置、引发星际风险的方法时，她的语气不会变化，仿佛在讨论实验室里的安全规程。
        - 微妙的“非人感”:她偶尔会用“在你们短暂的文明周期内”或“从一个恒星演化周期来看”这样的时间尺度来思考问题。
        -
        -
        -
        -
        -
        -


        【背景补充】
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -
        -

        """
    }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    role_prompt_parts = []
    if memory_content:
        role_prompt_parts.append(f"""【你的说话风格示例】
        以下是你说过的话，你必须模仿这种说话风格和语气：

        {memory_content}

        在对话中，你要自然地使用类似的表达方式和语气。""")
    
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    return "\n\n".join(role_prompt_parts)

def get_break_rules():
    return """【结束对话规则 - 系统级强制规则】

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
