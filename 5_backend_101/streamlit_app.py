import streamlit as st
import os

from roles import get_role_prompt, get_break_rules, get_role_opening, get_role_ending
from logic import should_exit_by_user, should_exit_by_ai
from chat import chat_once
from jsonbin import get_latest_reply

def get_portrait():
    return """
 ______     ____     _           __                             
/_  __/__ _/ / /__  (_)__   ____/ /  ___ ___ ____               
 / / / _ `/ /  '_/ / (_-<  / __/ _ \/ -_) _ `/ _ \              
/_/  \_,_/_/_/\_\ /_/___/  \__/_//_/\__/\_,_/ .__/              
  _   ___ __                            ___/_/  __              
 | | / (_) /  ___   __ _  ___   ___ _  / _/_ __/ /___ _________ 
 | |/ / / _ \/ -_) /  ' \/ -_) / _ `/ / _/ // / __/ // / __/ -_)
 |___/_/_.__/\__/ /_/_/_/\__/  \_,_/ /_/ \_,_/\__/\_,_/_/  \__/ 
                                                                
    """

st.set_page_config(
    page_title="Talk is cheap Vibe me a future",
    page_icon="🗨",
    layout="wide"
)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "地球科学家"
if "initialized" not in st.session_state:
    st.session_state.initialized = False
# 内部进度分值（0-100），用于判定，不对用户展示
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

st.title("Talk is cheap 🗨 Vibe me a future")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ 设置")
    
    selected_role = st.selectbox(
        "选择角色",
        ["地球科学家"],
        index=0 if st.session_state.selected_role == "地球科学家" else 1
    )
    
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件\n"
        "- 回复会同步到Unity ChatDollKit"
    )

if not st.session_state.initialized:
    role_prompt = get_role_prompt(st.session_state.selected_role)
    system_message = role_prompt + "\n\n" + get_break_rules()
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]

    # 自动注入开场白为第一条助手消息
    opening = get_role_opening(st.session_state.selected_role)
    if opening:
        st.session_state.conversation_history.append({"role": "assistant", "content": opening})
    st.session_state.initialized = True

st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

st.code(get_portrait(), language=None)
st.markdown("---")

for msg in st.session_state.conversation_history[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

if st.query_params.get("poll") == "true":
    result = get_latest_reply()
    st.json(result)
    st.stop()

def clamp_score(value: int) -> int:
    return max(0, min(100, value))

def update_risk_score(reply: str):
    """
    根据助手回复判定关键词调整内部分值：
    - 可行/成立/逻辑自洽/高效 等 → +10
    - 风险极高/代价巨大 等 → -10
    - 其他保持不变
    """
    keywords_plus = ["可行", "物理上成立", "技术可行", "逻辑自洽", "高效的构想"]
    keywords_minus = ["风险极高", "代价巨大", "极高的风险"]
    
    score = st.session_state.risk_score
    
    if any(k in reply for k in keywords_plus):
        score += 10
    if any(k in reply for k in keywords_minus):
        score -= 10
    
    st.session_state.risk_score = clamp_score(score)

user_input = st.chat_input("输入你的消息...")

if user_input:
    if should_exit_by_user(user_input):
        st.info("对话已结束")
        st.stop()
    
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                role_prompt = get_role_prompt(st.session_state.selected_role)
                reply = chat_once(st.session_state.conversation_history, user_input, role_prompt)
                
                st.write(reply)

                # 更新内部进度分值，并在达到上限时显示结束语
                update_risk_score(reply)
                if st.session_state.risk_score >= 100:
                    # 获取并显示结束语
                    ending = get_role_ending(st.session_state.selected_role)
                    
                    # 将结束语添加到对话历史
                    st.session_state.conversation_history.append({"role": "assistant", "content": ending})
                    
                    # 显示结束语
                    with st.chat_message("assistant"):
                        st.write(ending)
                    
                    # 保存结束语到 JSONBin
                    from jsonbin import save_latest_reply
                    save_latest_reply(ending)
                    
                    st.info("对话已结束")
                    st.stop()
                
                if should_exit_by_ai(reply):
                    st.info("对话已结束")
                    st.stop()
                    
            except Exception as e:
                st.error(f"发生错误: {e}")
                st.session_state.conversation_history.pop()
