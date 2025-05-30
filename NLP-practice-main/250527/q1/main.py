word_counter = dict()

# 단어가 key, 빈도수가 value로 구성된 딕셔너리 변수를 만드세요.
with open('D:/학습/250527/NLP-practice-main/250527/q1/text.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip()
        words = line.split()
        for word in words:
            if word in word_counter:
                word_counter[word] +=1
            else:
                word_counter[word] = 1


# 텍스트 파일에 내 모든 단어의 총 빈도수를 구해보세요.
total = sum(word_counter.values())

# 텍스트 파일 내 100회 이상 발생하는 단어를 리스트 형태로 저장하세요.
up_five = [word for word, count in word_counter.items() if count >= 100]


print(total)
print(up_five)