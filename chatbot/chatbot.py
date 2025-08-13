import torch
import streamlit as st
import time
import os
from transformers import AutoTokenizer, AutoModel

def load_model_and_tokenizer(local_dir: str = "./models/agro-nucleotide-transformer-1b"):
    """로컬에 저장된 모델과 토크나이저를 로드합니다."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(local_dir)
        model = AutoModel.from_pretrained(local_dir)
        return model, tokenizer
    except Exception as e:
        st.error(f"모델 로딩 중 오류 발생: {e}")
        return None, None

def preprocess_nucleotide_input(user_input: str) -> str:
    """사용자 입력을 뉴클레오타이드 서열 형태로 전처리합니다.""" 
    # DNA/RNA 서열만 추출 (A, T, G, C, U만 허용)
    valid_nucleotides = set('ATGCU')
    cleaned_input = ''.join([char.upper() for char in user_input if char.upper() in valid_nucleotides])
    
    if not cleaned_input:
        # 입력이 뉴클레오타이드 서열이 아닌 경우, 예시 서열 반환
        return "ATGCGATCGATCGATCG"
    
    return cleaned_input

def get_chatbot_response(user_input: str) -> str:
    """
    Agro-Nucleotide Transformer 모델을 사용하여 챗봇 응답을 생성합니다.
    
    Args:
        user_input (str): 사용자 입력 (DNA/RNA 서열 또는 일반 텍스트)
    
    Returns:
        str: 챗봇 응답
    """
    try:
        # 모델과 토크나이저 로드
        model, tokenizer = load_model_and_tokenizer()
        
        if model is None or tokenizer is None:
            return "모델을 로드할 수 없습니다. 먼저 모델을 다운로드해주세요."
        
        # 입력 전처리
        nucleotide_sequence = preprocess_nucleotide_input(user_input)
        
        # 뉴클레오타이드 서열이 너무 짧은 경우 패딩
        if len(nucleotide_sequence) < 16:
            nucleotide_sequence = nucleotide_sequence + "A" * (16 - len(nucleotide_sequence))
        
        # 토크나이제이션
        inputs = tokenizer(
            nucleotide_sequence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # 모델 추론
        model.eval()
        with torch.no_grad():
            outputs = model(**inputs)
            
            # 마지막 히든 스테이트에서 특성 추출
            last_hidden_states = outputs.last_hidden_state
            
            # 평균 풀링으로 서열 임베딩 생성
            sequence_embedding = torch.mean(last_hidden_states, dim=1)
            
            # 임베딩을 기반으로 응답 생성 (단순한 규칙 기반)
            embedding_norm = torch.norm(sequence_embedding).item()
            embedding_mean = torch.mean(sequence_embedding).item()
            
            # 응답 생성 로직
            if embedding_norm > 10:
                response_type = "복잡한 구조"
            elif embedding_norm > 5:
                response_type = "중간 복잡도"
            else:
                response_type = "단순한 구조"
            
            if embedding_mean > 0:
                tendency = "양성 특성"
            else:
                tendency = "음성 특성"
        
        # 응답 메시지 생성
        if len(user_input.strip()) == 0:
            return "안녕하세요! DNA/RNA 서열을 입력해주시면 분석해드리겠습니다."
        
        # 원본 입력이 뉴클레오타이드 서열인지 확인
        original_is_nucleotide = any(char.upper() in 'ATGCU' for char in user_input)
        
        if original_is_nucleotide:
            response = f"""
🧬 **뉴클레오타이드 서열 분석 결과**

**입력 서열**: {user_input[:50]}{'...' if len(user_input) > 50 else ''}

**처리된 서열**: {nucleotide_sequence[:30]}{'...' if len(nucleotide_sequence) > 30 else ''}

**서열 길이**: {len(nucleotide_sequence)} bp

**분석 결과**:
- 구조 복잡도: {response_type}
- 특성 경향: {tendency}
- 임베딩 노름: {embedding_norm:.3f}
- 평균 활성화: {embedding_mean:.3f}

이 서열은 농업 생명공학 관점에서 {response_type}를 가지며, {tendency}을 보입니다.
            """.strip()
        else:
            response = f"""
죄송합니다. 이 모델은 DNA/RNA 서열 분석에 특화되어 있습니다. 

**입력하신 내용**: {user_input[:100]}{'...' if len(user_input) > 100 else ''}

올바른 사용을 위해 다음과 같은 형태의 뉴클레오타이드 서열을 입력해주세요:
- 예시: ATGCGATCGATCGATCG
- 허용 문자: A, T, G, C, U

테스트용으로 임의의 서열로 분석한 결과:
- 구조 복잡도: {response_type}
- 특성 경향: {tendency}
            """.strip()
        
        return response
        
    except Exception as e:
        error_message = f"응답 생성 중 오류가 발생했습니다: {str(e)}"
        st.error(error_message)
        return "죄송합니다. 현재 서비스에 문제가 있습니다. 나중에 다시 시도해주세요."

def chatbot():
    chat_container = st.container()

    with chat_container:
        # 기존 메시지들 표시
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])


    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요...")


    # 사용자가 메시지를 입력했을 때
    if user_input:
        # 사용자 메시지를 세션에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 사용자 메시지 표시
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)
        
        # 봇 응답 생성
        with st.spinner("생각 중..."):
            time.sleep(1)  # 실제 응답을 기다리는 것처럼 보이게 하는 딜레이
            bot_response = get_chatbot_response(user_input)
        
        # 봇 응답을 세션에 추가
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # 봇 응답 표시
        with chat_container:
            with st.chat_message("assistant"):
                st.write(bot_response)
        
        # 페이지 새로고침으로 최신 메시지가 보이도록
        st.rerun()

def sidebar():
    # 사이드바에 추가 기능
    with st.sidebar:
        st.header("채팅 관리")
        
        # 대화 기록 개수 표시
        st.metric("총 메시지", len(st.session_state.messages))
        
        # 대화 기록 삭제 버튼
        if st.button("대화 기록 삭제", type="secondary"):
            st.session_state.messages = []
            st.rerun()