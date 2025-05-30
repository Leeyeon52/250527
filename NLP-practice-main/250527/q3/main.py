import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# 필요한 리소스 다운로드 (처음 한 번만 실행)
nltk.download('punkt')
nltk.download('stopwords')

test_sentences = [
    "i have looked forward to seeing this since i first saw it amoungst her work",
    "this is a superb movie suitable for all but the very youngest",
    "i first saw this movie when I was a little kid and fell in love with it at once",
    "i am sooo tired but the show must go on",
]

# 영어 stopwords 로딩
stopwords_set = set(stopwords.words('english'))
print("기본 stopwords 개수:", len(stopwords_set))

# 새로운 stopwords 추가
new_keywords = ['noone', 'sooo', 'thereafter', 'beyond', 'amoungst', 'among']
updated_stopwords = stopwords_set.union(new_keywords)
print("업데이트된 stopwords 개수:", len(updated_stopwords))

# 문장별 토큰화 및 stopwords 제거
tokenized_word = []
for sentence in test_sentences:
    tokens = word_tokenize(sentence.lower())  # 소문자 변환
    filtered = [word for word in tokens if word not in updated_stopwords and word.isalpha()]
    tokenized_word.append(filtered)

print("토큰화 및 stopword 제거 결과:")
print(tokenized_word)

# 첫 문장에 대해 stemming 적용
stemmed_sent = []
stemmer = PorterStemmer()
for word in tokenized_word[0]:
    stemmed_word = stemmer.stem(word)
    stemmed_sent.append(stemmed_word)

print("Stemming 결과 (첫 문장):")
print(stemmed_sent)
