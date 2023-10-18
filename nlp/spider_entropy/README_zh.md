[**中文**](./README_zh.md) | [**English**](./README.md)

<div id="top"></div>

# Spider & Entropy

该repo用于计算文本数据的熵，并提供了爬虫获取文本文件和数据处理的功能。

示例数据是爬取的中国新闻网，英文wikipedia和中文wikipedia，古诗文网的数据。分别对中英文文本进行了一定程度的文本清洗。

并使用jieba对中文分词，spacy对英文词性还原，opencc繁体转为简体。

## 安装依赖

在开始使用之前，确保你已经安装了以下依赖：

- Python 3.x
- 安装其他Python库（请参考`requirements.txt`文件）

你可以使用以下命令安装Python库：

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 📁 文件夹

```bash
├── data/ # 爬取到的数据
│   ├──news_zh # 中国新闻网 
│   ├──wiki_zh # 中文wikipedia
│   ├──wiki_en # 英文wikipedia
├── photos/ # 图
├── get_data_en # 爬取英文wikipedia
├── get_data_zh # 爬取中文wikipedia
├── get_news # 爬取中国新闻网
├── get_gushiwen # 爬取古诗文网
├── main # 计算熵，绘制图，验证齐夫定律
├── process_data # 处理数据，文本清洗，分词等
```

## 🔧 开始使用

### 快速开始

```bash
python -u main.py
```

### 爬取数据

根据get文件自行爬取数据，爬取的数据存放在data文件夹下
