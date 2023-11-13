import requests
from bs4 import BeautifulSoup
import re
from process_data import preprocess_text, preprocess_text_zh
import json
import time

en_base_url = 'https://en.wikipedia.org/wiki/'  # English Wikipedia
zh_base_url = 'https://zh.wikipedia.org/wiki/' # Chinese Wikipedia
# Wikipedia页面URL
url = 'https://en.wikipedia.org/wiki/Web_scraping'

visited_key_words = ['Film']
n = 0

def scrapeWikiArticle(url, key_word, out_path):
    # key_word = url.split('/')[-1]
    print(key_word)
    global n
    n += 1
    if n > 1000:
        return
    
    # 发送HTTP请求并获取页面内容
    response = requests.get(url + key_word)
    # 检查是否成功获取页面
    if response.status_code == 200:
        # 使用Beautiful Soup解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find(id="firstHeading")

        all_links = soup.find(id="bodyContent").find_all("a")
        
        # 找到页面主要内容
        paragraphs = soup.find(id="bodyContent").find_all("p")

        # 初始化一个空的文本字符串，用于存储处理后的内容
        cleaned_text = ""

        # 提取段落文本并进行清洗
        for paragraph in paragraphs:
            text = paragraph.get_text()  # 获取段落文本

            text = preprocess_text(text)
            # 使用正则表达式去除特殊字符和多余空格
            cleaned_text += re.sub(r'[^\w\s]', ' ', text).strip()
            # cleaned_text = re.sub(r'[^\w\s]', ' ', text)

        # 打印清洗后的文本
        # print(cleaned_text)
        with open(out_path, "a", encoding="utf-8") as f:
            json.dump({key_word:cleaned_text}, f, ensure_ascii=False)
            f.write("\n")
            
        for link in all_links:
            try:
                if link['href'].find("/wiki/") == -1:
                    continue
            except:
                continue
            # print(link['href'])
            key_word = link['href'].split('/')[-1]
            if key_word in visited_key_words:
                continue
            if '.' in key_word:
                continue
            if ':' in key_word:
                continue
            visited_key_words.append(key_word)
            # 关闭HTTP连接
            response.close()
            time.sleep(2)
            try:
                scrapeWikiArticle(url, key_word, out_path)
            except:
                continue
    else:
        print('Unable to get page')
        
scrapeWikiArticle(en_base_url, 'Film', "data/wiki0.json")
