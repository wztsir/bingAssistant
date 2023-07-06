import re
from googletrans import Translator

def translate_text(text, dest='en'):
    # 使用正则表达式判断文本是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', text):
        translator = Translator()
        translation = translator.translate(text, dest=dest)
        return translation.text
    else:
        return text


text1 = "你怎么看待乌克兰局势"

translated_text1 = translate_text(text1)

print(translated_text1)
