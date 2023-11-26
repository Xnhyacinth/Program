'''
Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2023-11-20 05:38:21
'''

# 读取整个文章
with open("data/news.2017.zh.shuffled.deduped", "r", encoding="utf-8") as file:
    full_text = file.readlines()

# 将文章分割成句子
# sentences = full_text.split("。")  # 这只是一个简单的分割方法，实际中可能需要更复杂的方法来处理不同的句子结构

# 提取最后一千句
trai_set = full_text[:-1000]
test_set = full_text[-1000:]

# 将提取的句子写入一个新文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("".join(test_set))
with open("train.txt", "w", encoding="utf-8") as f:
    f.write("".join(trai_set))