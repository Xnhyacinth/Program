# 爬虫获取文本，并计算文本数据的熵和验证齐夫定律

该repo用于计算文本数据的熵，并提供了爬虫获取文本文件和数据处理的功能。

## 安装依赖

在开始使用之前，确保你已经安装了以下依赖：

- Python 3.x
- 安装其他Python库（请参考`requirements.txt`文件）

你可以使用以下命令安装Python库：

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 📁 Folder

```bash
├── data/ # 爬取到的数据 
├── photos/ # 图
├── get_data_en # 爬取英文wikipedia
├── get_data_zh # 爬取中文wikipedia
├── get_news # 爬取中国新闻网
├── get_gushiwen # 爬取古诗文网
├── main # 计算熵，绘制图，验证齐夫定律
├── process_data # 处理数据，文本清洗，分词等
```

## 🔧 Get started
### QuickStart
```
python -u main.py
```

### 爬取数据
根据get文件自行爬取数据，爬取的数据存放在data文件夹下
