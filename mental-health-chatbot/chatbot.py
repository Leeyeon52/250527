import streamlit as st
from streamlit_chat import message # 설치(파이썬 3.8 이상에서만 작동)
import pandas as pd
from sentence_transformers import SentenceTransformer #sentence_transformer 설치 필요
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
# pip install numpy==1.23.0

@st.cache_resource
#@st.cache(allow_output_mutation=True) # 한 번만 로드해서 사용
def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

@st.cache_resource
#@st.st.cache(allow_output_mutation=True)
def get_dataset():
    df = pd.read_csv('wellness_dataset.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
    return df

model = cached_model()
df = get_dataset()

st.header('심리상담 챗봇')
st.markdown("Elice Chatbot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = [] # 대화한 내용 저장

if 'past' not in st.session_state:
    st.session_state['past'] = [] # 지난 대화 저장

with st.form('form', clear_on_submit=True): # 사용자 입력 폼
    user_input = st.text_input('당신: ', '')
    submitted = st.form_submit_button('전송')

if submitted and user_input:
    embedding = model.encode(user_input)

    # 임베딩 정규화
    embedding_norm = np.linalg.norm(embedding)
    df['distance'] = df['embedding'].apply(
        lambda x: np.dot(embedding, x) / (embedding_norm * np.linalg.norm(x))
    )
    
    answer = df.loc[df['distance'].idxmax()]

    st.session_state.past.append(user_input)
    st.session_state.generated.append(answer['시스템문장1'])

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if len(st.session_state['generated']) > i:
        message(st.session_state['generated'][i], key=str(i) + '_bot')
