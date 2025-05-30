import pandas as pd
from gensim.models import Word2Vec

def load_data(filepath):
    data = pd.read_csv(filepath, delimiter=';', header=None, names=['sentence','emotion'])
    data = data['sentence']

    gensim_input = []
    for text in data:
        gensim_input.append(text.rstrip().split())
    return gensim_input

input_data = load_data("D:/학습/250527/NLP-practice-main/250527/q4/emotions_train.txt")


# word2vec 모델을 학습하세요.
model = Word2Vec(
    sentences=input_data,
    vector_size=300,
    window=2,
    min_count=1,
    workers=4,
    epochs=10
)


# happy와 유사한 단어를 확인하세요.
similar_happy = model.wv.most_similar('happy', topn=10)

print(similar_happy)

# sad와 유사한 단어를 확인하세요.
similar_sad = model.wv.most_similar('sad', topn=10)
print(similar_sad)

# 단어 good과 bad의 임베딩 벡터 간 유사도를 확인하세요.
similar_good_bad = model.wv.similarity('good','bad')

print(similar_good_bad)

# 단어 sad과 lonely의 임베딩 벡터 간 유사도를 확인하세요.
similar_sad_lonely = model.wv.similarity('sad','lonely')

print(similar_sad_lonely)

# happy의 임베딩 벡터를 확인하세요.
wv_happy = model.wv['happy']

print(wv_happy)
