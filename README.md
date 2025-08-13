<img alt="Python" src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" height="20"/> <img alt="huggingface" src="https://img.shields.io/badge/huggingface-FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=white" height="20"/> <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white" height="20"/> <img alt="LangChain" src="https://img.shields.io/badge/LangChain-1C3C3C.svg?style=for-the-badge&logo=LangChain&logoColor=white" height="20"/> <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-1C3C3C.svg?style=for-the-badge&logo=LangGraph&logoColor=white" height="20"/>

</br>

# 🧬 BioChat

### 프로젝트 개요
- **전체 개발 기간**: 2025.08.05 - 개발 중

</br>

## 📦 다운로드 및 설치

### 1. github clone
```python
git clone https://github.com/yrc00/BioChat.git
cd BioChat

```

</br>

### 2. 가상환경
```python
conda create -n biochat python=3.11
conda activate biochat
pip install -r requirements.txt
```

</br>

### 3. 모델 다운로드
```python
python3 ./models/model_download.py
```
- model_download.py를 실행하기 전 `.streamlit/secrets.toml`에 `HUGGINGFACE_API_KEY`를 입력

</br>

### 4. 어플리케이션 실행
```python
streamlit run app.py
```