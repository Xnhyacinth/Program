[**中文**](./README_zh.md) | [**English**](./README.md)

<div id="top"></div>

# Spider & Entropy

The repo is used to calculate the entropy of text data, and provides functions for crawlers to obtain text files and data processing.

The example data are crawled from China News Network, English wikipedia and Chinese wikipedia, and Ancient Poetry Network. A certain degree of text cleaning was performed on the Chinese and English texts respectively.

And use jieba to Chinese participle, spacy to English lexical reduction, opencc traditional to simplified.

## Dependencies

Before getting started, make sure you have the following dependencies installed:

- Python 3.x
- Install other Python libraries (see the `requirements.txt` file)

You can install Python libraries using the following command:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 📁 Folder

```bash
├── data/ # Crawled data
│   ├──news_zh # Chinese news network 
│   ├──wiki_zh # Chinese wikipedia
│   ├──wiki_en # English wikipedia
├── photos/ # diagrams
├── get_data_en # Crawl English wikipedia
├── get_data_zh # Crawl Chinese wikipedia
├── get_news # Crawl Chinese wikipedia
├── get_gushiwen # Crawl ancient Chinese wikipedia
├── main # Calculating entropy, plotting graphs, verifying Ziff's law.
├── process_data # Process data, text cleaning, split words, etc.
```

## 🔧 Get started

### QuickStart

run to calculate the entropy and draw diagrams.

```bash
python -u main.py
```

### Data

Crawl the data according to the get file itself, the crawled data is stored in the data folder.
