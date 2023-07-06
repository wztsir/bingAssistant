from gensim import corpora, models
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_topics(sentence, num_topics=2, num_words=4):
    # 分词和去除停用词
    stop_words = set(stopwords.words('english'))  # 如果是中文，请使用中文停用词表
    tokens = word_tokenize(sentence)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # 构建文本语料库
    dictionary = corpora.Dictionary([filtered_tokens])
    corpus = [dictionary.doc2bow(filtered_tokens)]

    # 使用LDA模型提取主题
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    # 获取每个主题的关键词
    topics = lda_model.print_topics(num_topics=num_topics, num_words=num_words)

    # 提取关键词
    keywords = []
    for topic in topics:
        topic_words = [word.split('*')[1].strip().replace('"', '') for word in topic[1].split('+')]
        keywords.extend(topic_words)

    return keywords


# 示例句子
# sentence = "What do you think of the situation in Ukraine"
# sentence = "What do you think of the situation in Ukraine"
sentence = "What do you think of China's persistently high unemployment rate"

# 提取主题关键词
topics = extract_topics(sentence, num_topics=2, num_words=4)

# 打印提取到的主题关键词
print(topics)
