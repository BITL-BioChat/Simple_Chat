import streamlit as st
from chatbot.chatbot import chatbot, sidebar

# 챗봇 타이틀
st.set_page_config(page_title="BioChat", page_icon="🧬", layout="centered")

# 세션 상태로 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

if __name__ == "__main__":
    # 제목
    st.title("🧬 Welcome to BioChat!")
    chatbot()
    sidebar()
    
