import streamlit as st
from streamlit_chat import message
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import random

@st.cache_resource
def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

@st.cache_data
def get_dataset(_model):  # _model로 변경하여 캐시 무시 대상 지정
    df = pd.read_csv('wellness_dataset.csv')
    df['combined'] = df[['사람문장1', '사람문장2', '사람문장3']].fillna('').agg(' '.join, axis=1)
    df['embedding'] = df['combined'].apply(lambda x: _model.encode(x))
    # 시스템문장들도 NaN 대비 빈 문자열 처리
    df['시스템문장1'] = df['시스템문장1'].fillna('')
    df['시스템문장2'] = df['시스템문장2'].fillna('')
    df['시스템문장3'] = df['시스템문장3'].fillna('')
    return df

model = cached_model()
df = get_dataset(model)

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

    df['similarity'] = df['embedding'].apply(
        lambda x: np.dot(embedding, x) / (embedding_norm * np.linalg.norm(x))
    )

    answer = df.loc[df['similarity'].idxmax()]

    # 시스템문장 3개 중 하나를 랜덤 선택 (빈 문자열 제외)
    possible_answers = [answer['시스템문장1'], answer['시스템문장2'], answer['시스템문장3']]
    possible_answers = [a for a in possible_answers if a.strip() != '']
    if possible_answers:
        selected_answer = random.choice(possible_answers)
    else:
        selected_answer = "죄송해요, 적절한 답변을 찾지 못했어요."

    st.session_state.past.append(user_input)
    st.session_state.generated.append(selected_answer)

for i in range(len(st.session_state['past'])):
    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
    if len(st.session_state['generated']) > i:
        message(st.session_state['generated'][i], key=str(i) + '_bot')
