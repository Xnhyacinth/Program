import json
import collections
import math
import re
import numpy as np
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.probability import FreqDist
# 下载NLTK停用词和示例文本数据
nltk.download('stopwords')
nltk.download('punkt')
#'data/wiki0.json'
def load_data(data_path, n):
    text = ''
    all_docs = dict()
    with open(data_path, 'r', encoding="utf-8") as f:
        # content = f.read(1024)
        for line in f:
            data = json.loads(line)
            # print(data.keys())
            # if list(data.keys())[0] not in list(all_docs.keys()):
            all_docs[list(data.keys())[0]] = list(data.values())[0]
            text += list(data.values())[0]
            if len(text.encode('utf-8')) > 1024 * 1024 * n:
                break
                    
                
    # print(all_docs.keys())
    # return ''.join([char for char in text if char.isprintable()])
    return text
# print(data)

def calculate_probabilities_and_entropy(text, lang):
    # 统计每个字母的出现次数
    text = re.sub(r'[\x80-\xff]', '', text)
    if lang == 'en':
        text = re.sub(r'[^a-zA-Z\s\n]', '', text)
    letter_counts = collections.Counter(text)
    if lang == 'zh':
        # 找到最大值
        max_value = max(letter_counts.values())

        # 找到具有最大值的键
        max_key = [key for key, value in letter_counts.items() if value == max_value][0]
        print(max_key.encode('utf-8'))
        # 删除具有最大值的键值对
        del letter_counts[max_key]
        # 计算样本的总字母数
        total_letters = len(text) - max_value
    else:
        total_letters = len(text)
    print(total_letters)
    # 初始化存储概率和熵的变量
    probabilities = {}
    entropy = 0.0
    entropys = {}
    # 计算每个字母的概率和贡献到熵的部分
    for letter, count in letter_counts.items():
        probability = count / total_letters
        probabilities[letter] = probability
        entropy -= probability * math.log2(probability)
        entropys[letter] = -probability * math.log2(probability)

    return probabilities, entropy, entropys

def draw(text, type):
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum() and word not in stopwords.words('chinese')]
    # print(words)
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False

    # print(matplotlib.get_cachedir())
    # 计算单词频率
    fdist = FreqDist(words)

    # 将频率分布的结果按照频率从高到低排序
    sorted_fdist = sorted(fdist.items(), key=lambda item: item[1], reverse=True)
    # 绘制齐夫定律验证图
    rank = np.arange(1, len(sorted_fdist) + 1)
    frequency = [item[1] for item in sorted_fdist]
    plt.figure(figsize=(12, 6))
    plt.plot(rank, frequency)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Rank (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title('Zipf\'s Law Verification')
    plt.grid(True)
    # 添加图例
    plt.legend(loc='upper right')
    plt.savefig(f'photos/a_{type}.png')  
    plt.savefig(f'photos/a_{type}.pdf', format='pdf')

def draw_all(text_zh, text_en, text_news):
    ranks, frequencys = [], []
    ranks_o, frequencys_o = [], []
    for text in [text_zh, text_en, text_news]:
        words = nltk.word_tokenize(text)
        words = [word.lower() for word in words if word.isalnum() and word not in stopwords.words('chinese')]
        # print(words)
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False

        # print(matplotlib.get_cachedir())
        # 计算单词频率
        fdist = FreqDist(words)

        # 将频率分布的结果按照频率从高到低排序
        sorted_fdist = sorted(fdist.items(), key=lambda item: item[1], reverse=True)
        # 绘制齐夫定律验证图
        rank = np.arange(1, len(sorted_fdist) + 1)
        frequency = [item[1] for item in sorted_fdist]
        ranks.append(rank)
        frequencys.append(frequency)
        # ranks_o.append(np.log(rank))
        # frequencys_o.append(np.log(frequency))
    # 创建第一个子图
    plt.subplot(211)  # 2行1列的子图，第1个子图
    # plt.figure(figsize=(12, 6))
    
    plt.plot(ranks[0], frequencys[0], linestyle='-', color='#FA7F6F', label='中文wikipedia(log)', linewidth=2)
    plt.plot(ranks[1], frequencys[1], linestyle='-', color='#8ECFC9', label='英文wikipedia(log)', linewidth=2)
    plt.plot(ranks[2], frequencys[2], linestyle='-', color='#FFBE7A', label='中国新闻网(log)', linewidth=2)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Rank (log scale)')
    plt.ylabel('Frequency (log scale)')
    plt.title('Zipf\'s Law Verification')
    plt.grid(True)
    # 添加图例
    plt.legend(loc='upper right')
    
    plt.subplot(212)  # 2行1列的子图，第2个子图
    plt.plot(ranks[0], frequencys[0], linestyle='-', color='#FA7F6F', label='中文wikipedia', linewidth=2)
    plt.plot(ranks[1], frequencys[1], linestyle='-', color='#8ECFC9', label='英文wikipedia', linewidth=2)
    plt.plot(ranks[2], frequencys[2], linestyle='-', color='#FFBE7A', label='中国新闻网', linewidth=2)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.title('Zipf\'s Law Verification')
    plt.grid(True)
    # 添加图例
    plt.legend(loc='upper right')
    # 调整子图的布局，避免重叠
    plt.tight_layout()
    plt.savefig(f'photos/aa.png')  
    plt.savefig(f'photos/aa.pdf', format='pdf')

def draw_p(probabilities, entropys):
    # 将字母和对应的熵值分离为两个列表
    letters = list(probabilities.keys())

    # 创建一个排序后的字母列表，以便按字母顺序绘制曲线
    sorted_letters = sorted(letters)

    # 按字母顺序重新排列熵值列表
    sorted_probability = [probabilities[letter] * 10 for letter in sorted_letters]
    sorted_entropy = [entropys[letter] for letter in sorted_letters]

    # 创建 x 轴，即字母
    x = np.arange(len(sorted_letters))
    
    # # 创建曲线图
    # fig, ax1 = plt.subplots(figsize=(10, 6))

    # # 绘制概率曲线，使用左侧纵坐标轴
    # ax1.plot(x, sorted_probability, marker='o', linestyle='-', color='b', label='概率')
    # ax1.set_xlabel('字母')
    # ax1.set_ylabel('概率', color='b')
    # ax1.tick_params(axis='y', labelcolor='b')

    # # 创建第二个纵坐标轴，用于信息熵曲线
    # ax2 = ax1.twinx()
    # ax2.plot(x, sorted_entropy, marker='x', linestyle='-', color='r', label='信息熵')
    # ax2.set_ylabel('信息熵', color='r')
    # ax2.tick_params(axis='y', labelcolor='r')

    # plt.xticks(x, sorted_letters)
    # # 标注信息熵的值
    # for i, entropy in enumerate(sorted_entropy):
    #     ax2.annotate(f'Entropy: {entropy:.2f}', (i, entropy), textcoords="offset points", xytext=(0, 10), ha='center')

    # # 添加图例
    # lines, labels = ax1.get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax1.legend(lines + lines2, labels + labels2, loc='upper right')

    # plt.title('不同字母的概率和信息熵')
    
    # 创建柱状图
    # plt.figure(figsize=(10, 6))
    # plt.bar(x, sorted_probability, color='#FA7F6F', alpha=0.7)
    # plt.xticks(x, sorted_letters)
    # plt.xlabel('字母')
    # plt.ylabel('概率')
    # plt.title('不同字母的概率柱状图')
    # 添加标注和标出数值
    # for i, prob in enumerate(sorted_probability):
    #     if prob > 0.001:
    #         plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    # plt.grid(True)
    # plt.legend(loc='upper right')
    # # 创建 x 轴，即字母
    # x = np.arange(len(sorted_letters))

    # # 创建曲线图
    plt.figure(figsize=(10, 6))
    plt.plot(x, sorted_probability, linestyle='-', color='#FFBE7A', label='概率')
    # plt.xticks(x, sorted_letters)
    plt.xlabel('汉字')
    plt.ylabel('概率')
    plt.title('不同汉字的概率')
    # plt.grid(True)
    # # 添加图例
    plt.legend(loc='upper right')
    plt.savefig('photos/b1.png')
    plt.savefig('photos/b1.pdf', format='pdf')

def draw_hs(hs, hs_w, hs_e):
    # 创建 x 轴，即字母
    x = np.arange(2, len(hs) * 2 + 1, 2)
    # # 创建曲线图
    plt.figure(figsize=(10, 6))
    plt.plot(x, hs, linestyle='-', color='#82B0D2', label='中国新闻网', marker='o', linewidth=2)
    plt.plot(x, hs_w, linestyle='-', color='#8ECFC9', label='中文wikipedia', marker='*', linewidth=2)
    plt.plot(x, hs_e, linestyle='-', color='#FFBE7A', label='英文wikipedia', marker='+', linewidth=2)
    # plt.xticks(x, sorted_letters)
    plt.xlabel('大小(M)')
    plt.ylabel('熵')
    # plt.title('不同汉字的概率')
    # plt.grid(True)
    # # 添加图例
    plt.legend(loc='upper right')
    plt.savefig('photos/hs.png')
    plt.savefig('photos/hs.pdf', format='pdf')

if __name__ == '__main__':
    hs, hs_w, hs_e = [], [], []
    for i in range(2, 39, 2):
        text = load_data('data/news_zh.json', i)

        # text = re.sub(r'[^a-zA-Z\s\n]', '', text)
        # 使用正则表达式去除非字母字符
        # text = "This is a sample 123 string with special characters!@#\nAnd here is a new line."

        # 调用函数计算概率和熵
        probabilities, entropy, entropys = calculate_probabilities_and_entropy(text, 'zh')
        # 打印每个字母的概率
        # print("字母概率:")
        # for letter, probability in probabilities.items():
        #     print(f"{letter}: {probability:.4f}  {entropys[letter]}")
        hs.append(entropy)
        # 打印熵
        print(f"熵: {entropy:.4f}")
    text_news = text
    for i in range(2, 39, 2):
        text = load_data('data/wiki0.json', i)

        # text = re.sub(r'[^a-zA-Z\s\n]', '', text)
        # 使用正则表达式去除非字母字符
        # text = "This is a sample 123 string with special characters!@#\nAnd here is a new line."

        # 调用函数计算概率和熵
        probabilities, entropy, entropys = calculate_probabilities_and_entropy(text, 'en')
        # 打印每个字母的概率
        # print("字母概率:")
        # for letter, probability in probabilities.items():
        #     print(f"{letter}: {probability:.4f}  {entropys[letter]}")
        hs_e.append(entropy)
        # 打印熵
        print(f"熵: {entropy:.4f}")
    text_en = text
    for i in range(2, 39, 2):
        text = load_data('data/wiki1.json', i)

        # text = re.sub(r'[^a-zA-Z\s\n]', '', text)
        # 使用正则表达式去除非字母字符
        # text = "This is a sample 123 string with special characters!@#\nAnd here is a new line."

        # 调用函数计算概率和熵
        probabilities, entropy, entropys = calculate_probabilities_and_entropy(text, 'zh')
        # 打印每个字母的概率
        # print("字母概率:")
        # for letter, probability in probabilities.items():
        #     print(f"{letter}: {probability:.4f}  {entropys[letter]}")
        hs_w.append(entropy)
        # 打印熵
        print(f"熵: {entropy:.4f}")
        # draw(text)
        # draw_p(probabilities, entropys)
    
    # 画图
    draw_all(text, text_en, text_news)
    draw_hs(hs, hs_w, hs_e)
    