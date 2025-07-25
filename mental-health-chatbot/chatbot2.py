import streamlit as st
from streamlit_chat import message
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

@st.cache_resource
def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

@st.cache_data
def get_dataset():
    df = pd.read_csv('wellness_dataset.csv')
    df = df[['사람문장1', '시스템문장1']].dropna()
    df['embedding'] = df['사람문장1'].apply(lambda x: model.encode(x))
    return df

model = cached_model()
df = get_dataset()

st.header('심리상담 챗봇')
st.markdown("Elice Chatbot")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('당신: ', '')
    submitted = st.form_submit_button('전송')

if submitted and user_input:
    embedding = model.encode(user_input)
    embedding_norm = np.linalg.norm(embedding)

    df['distance'] = df['embedding'].apply(
        lambda x: np.dot(embedding, x) / (embedding_norm * np.linalg.norm(x))
    )

    answer = df.loc[df['distance'].idxmax()]

    st.session_state.past.append(user_input)
    st.session_state.generated.append(answer['시스템문장1'])  # 챗봇 응답 문장

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if len(st.session_state['generated']) > i:
        message(st.session_state['generated'][i], key=str(i) + '_bot')
