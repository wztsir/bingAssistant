import spacy

# 命名实体识别
def extract_adjectives_and_nouns(sentence):
    nlp = spacy.load("en_core_web_sm")
    # 对句子进行命名实体识别
    doc = nlp(sentence)

    # 提取形容词和名词
    adjectives = []
    nouns = []
    for token in doc:
        if token.pos_ == "ADJ":
            adjectives.append(token.text)
        elif token.pos_ == "NOUN":
            nouns.append(token.text)

    # 按照输入语句的顺序组合形容词和名词
    combined = []
    for word in sentence.split():
        if word in adjectives:
            combined.append(word)
        elif word in nouns:
            combined.append(word)

    return " ".join(combined)

sentence = "What do you think of China's persistently high unemployment rate"
combined_words = extract_adjectives_and_nouns(sentence)
print("主题:", combined_words)

