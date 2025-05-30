import re
from collections import defaultdict

word_counter = defaultdict(int)
regex = re.compile('[^a-zA-Z]')  # 알파벳(a~z, A~Z)을 제외한 모든 문자 제거

# 텍스트 파일 열기 (필요시 절대 경로로 수정 가능)
with open('D:/학습/250527/NLP-practice-main/250527/q2/text.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # 1. 소문자 변환
        line = line.lower()
        # 2. 특수문자 및 숫자 제거
        line = regex.sub(' ', line)
        # 3. 공백 기준으로 단어 분리
        words = line.split()
        for word in words:
            word_counter[word] += 1

# 단어 "the"의 빈도수
count = word_counter['the']

print(count)
