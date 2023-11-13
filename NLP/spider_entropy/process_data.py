import pandas as pd
import spacy
import numpy as np
import jieba
import re
from opencc import OpenCC
# 加载spaCy英语语言模型
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # 使用spaCy进行文本处理
    doc = nlp(text)

    # 初始化一个空的字符串，用于存储处理后的文本
    cleaned_text = []

    for token in doc:
        # 去除停用词和标点符号
        if not token.is_stop and not token.is_punct:
            # 进行词形还原，并将词汇转换为小写
            cleaned_text.append(token.lemma_.lower())

    # 将处理后的文本拼接成字符串
    cleaned_text = ' '.join(cleaned_text)
    return cleaned_text


def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':  # 判断一个uchar是否是汉字
        return True
    else:
        return False

def allcontents(contents):
    content = ''
    for i in contents:
        if is_chinese(i):
            content = content+i
    return content

def preprocess_text_zh(text):
    text = text.replace(' ','')   # 去掉文本中的空格
    # text = allcontents(text) # 去掉非中文字符
    pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^a-z^A-Z^0-9]")
    text = re.sub(pattern, '', text)
    text = ''.join(text.split())
    tt = OpenCC('t2s')  # 繁转简
    text = tt.convert(text)
    # 分词
    words = jieba.cut(text)

    # 将分词结果拼接成字符串
    cleaned_text = " ".join(words)
    return cleaned_text
# # 示例文本
# text = "This is an example text with multiple words. Running, jumped, and eats are words."

# # 对文本进行处理
# cleaned_text = preprocess_text(text)

# # 打印处理后的文本
# print(cleaned_text)