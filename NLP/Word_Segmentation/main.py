'''
Copyright (c) 2024 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2024-01-02 06:56:23
'''
import jieba
import time
from collections import Counter
from collections import defaultdict

def get_dicts():
    # 打开文本文件并读取内容
    with open("data/Corpus.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # 按行分隔每一行的单词
    words_per_line = [line.split() for line in lines]
    # words = [item for sublist in words_per_line for item in sublist]
    # 输出分隔后的单词

    with open("data/dicts.txt", "w", encoding="utf-8") as file:
        for line in words_per_line:
            for word in line:
                file.write(word + "\n")
                
    with open("data/dicts.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    words_per_line = [line.split()[0] for line in lines]
    pos = [line.split()[1] for line in lines]
    print(words_per_line[:5])
    word_freq = Counter(words_per_line)
    with open("data/dicts_f.txt", "w", encoding="utf-8") as file:
        for word, freq in word_freq.items():
            file.write(f"{word}\t{freq}\n")

def get_jieba():
    # 加载自定义词典
    jieba.load_userdict("data/dicts_f.txt")

    # 示例文本
    text = "土耳其被曝秘密试射俄制S400防空导弹 美方高层放出狠话"

    # 分词（精确模式）
    start_time = time.time()
    seg_result = jieba.lcut(text)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 输出分词结果和性能分析信息
    print("分词结果：" + " / ".join(seg_result))
    print(f"分词耗时：{elapsed_time:.4f} 秒")

    # 性能分析
    word_freq = Counter(seg_result)
    print("\n词频统计：")
    # for word, freq in word_freq.items():
    #     print(f"{word}: {freq}")

get_jieba()