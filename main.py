import requests
import openai
import re
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

openai.api_key = 'XXXX'
news_api_key = '24b599f0d4ab4a3aa9bbd34cb40539be'


def process_spaces(text):
    text = text.replace(
        ' ,', ',').replace(
        ' .', '.').replace(
        ' ?', '?').replace(
        ' !', '!').replace(
        ' ;', ';').replace(
        ' \'', '\'').replace(
        ' ’ ', '\'').replace(
        ' :', ':').replace(
        '<newline>', '\n').replace(
        '`` ', '"').replace(
        ' \'\'', '"').replace(
        '\'\'', '"').replace(
        '.. ', '... ').replace(
        ' )', ')').replace(
        '( ', '(').replace(
        ' n\'t', 'n\'t').replace(
        ' i ', ' I ').replace(
        ' i\'', ' I\'').replace(
        '\\\'', '\'').replace(
        '\n ', '\n').replace(
        '\xa0', ' '
    ).strip()
    text = text.replace('\r\n', '\n').replace('\\n', '').replace('!\n', '')
    return re.sub('\n+', '\n', text)


def preprocess_context(context):
    # 删除换行符
    context = [text.replace('\n', ' ') for text in context]

    # 删除重复字符串
    context = list(set(context))

    # 限制字符串长度在50到500之间
    context = [text for text in context if len(text) < 500 and len(text) >= 50]

    # 进行额外的预处理步骤
    context = [process_spaces(text) for text in context]

    return context


def ask_question(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides news answers."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": context}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer


def translate_text(text, dest='en'):
    # 使用正则表达式判断文本是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', text):
        user_question = "将下面句子用简洁的语言翻译成英文"
        answer = ask_question(user_question, text)
        return answer
    else:
        return text


def getTheme(text):
    user_question = "Use no more than 5 words to describe the topic of this sentence:"
    context = text
    answer = ask_question(user_question, context)
    print(answer)
    return answer


def sort_news_list(query, context):
    # 加载预训练的BERT模型和tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # 对查询字符串进行编码和嵌入
    query_tokens = tokenizer.encode(query, add_special_tokens=True)
    query_input = torch.tensor([query_tokens])
    with torch.no_grad():
        query_embedding = model(query_input)[0].squeeze(0)

    # 对新闻列表进行编码和嵌入
    news_embeddings = []
    for text in context:
        text_tokens = tokenizer.encode(text, add_special_tokens=True)
        text_input = torch.tensor([text_tokens])
        with torch.no_grad():
            text_embedding = model(text_input)[0].squeeze(0)
        news_embeddings.append(text_embedding)

    # 将查询向量重复扩展到与新闻向量列表的长度相同
    query_embedding = query_embedding.repeat(len(news_embeddings), 1)

    # 计算查询与新闻之间的余弦相似度
    scores = cosine_similarity(query_embedding, torch.stack(news_embeddings))

    # 将得分和新闻列表关联并进行排序
    sorted_news_list = sorted(zip(context, scores.squeeze(0)), key=lambda x: x[1], reverse=True)
    sorted_news_list = [news for news, _ in sorted_news_list]

    return sorted_news_list


def get_news(query):
    # 使用News API获取相关新闻
    # news_api_key = 'YOUR_NEWS_API_KEY'
    news_api_url = f'https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}'
    response = requests.get(news_api_url)
    data = response.json()
    articles = data['articles']
    context = []
    for article in articles:
        description = article['description']
        context.append(description)
    context = preprocess_context(context)
    print(context)
    # context = sort_news_list(query, context)
    joined_string = ', '.join(context[:5])
    return joined_string


user_question = input("")
AS = getTheme(user_question)
print(AS)
news = get_news(AS)
# 新闻排序
print(news)

answer = ask_question(user_question, news)
print("问题的答案：", answer)
