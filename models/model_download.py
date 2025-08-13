import streamlit as st
from transformers import AutoModel, AutoTokenizer
import os

# Hugging Face API Key
HUGGINGFACE_API_KEY = st.secrets["HUGGINGFACE_API_KEY"]

# 모델 이름
model_name = 'InstaDeepAI/agro-nucleotide-transformer-1b'

# 저장할 로컬 디렉토리
local_dir = "./models/agro-nucleotide-transformer-1b"
os.makedirs(local_dir, exist_ok=True)

# 모델과 토크나이저 로드 및 저장
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# 로컬에 저장
tokenizer.save_pretrained(local_dir)
model.save_pretrained(local_dir)
print(f"모델과 토크나이저가 {local_dir}에 저장되었습니다.")