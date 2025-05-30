from gensim.models import FastText
import pandas as pd

# Emotions dataset for NLP 데이터셋을 불러오는 load_data() 함수입니다.
def load_data(filepath):
    data = pd.read_csv(filepath, delimiter=';', header=None, names=['sentence','emotion'])
    data = data['sentence']

    gensim_input = []
    for text in data:
        gensim_input.append(text.rstrip().split())

    return gensim_input

input_data = load_data("D:/학습/250527/NLP-practice-main/250527/q5/emotions_train.txt")

# fastText 모델을 학습하세요.
model = FastText(
    sentences=input_data,
    window=3,
    vector_size=100,
    min_count=10,
    epochs=10
)

# day와 유사한 단어 10개를 확인하세요.
similar_day = model.wv.most_similar('day', topn=10)

print(similar_day)

# night와 유사한 단어 10개를 확인하세요.
similar_night = model.wv.most_similar('night', topn=10)

print(similar_night)

# elllllllice의 임베딩 벡터를 확인하세요.
wv_elice = model.wv["elllllllice"]
print(similar_day)
print(similar_night)
print(wv_elice)