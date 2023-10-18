# import openpyxl
import json
import requests
from lxml import etree
from tqdm import tqdm

from process_data import preprocess_text_zh
 
 
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
 
 
# 组合日期链接
def cnew_url():
    urls = []
    for m in range(1, 9):
        for i in range(1, 25):
            if i < 10:
                url = f'https://www.chinanews.com.cn/scroll-news/2023/0{m}0' + str(i) + '/news.shtml'
            else:
                url = f'https://www.chinanews.com.cn/scroll-news/2023/0{m}' + str(i) + '/news.shtml'
            urls.append(url)
    return urls
 
 
def cnew_data(urls, out_path):
    for url in urls:
        links = []
        # 发起请求,获取页面里面的新闻链接
        req = requests.get(url.replace('\n', ''), headers=headers)
        # 设置网页编码，不设置会乱码
        req.encoding = 'utf8'
        ht = etree.HTML(req.text)
        # 获取分类的数据还有正文链接
        fl = ht.xpath("//div[@class='dd_lm']/a/text()")
        lj = ht.xpath("//div[@class='dd_bt']/a/@href")
        # 链接有两种格式，分别组合成可以用的
        for j in lj:
            if j[:5] == '//www':
                links.append('https:' + j)
            else:
                links.append('https://www.chinanews.com.cn/' + j)
        n = 0
        for link in tqdm(links):
            try:
                data = []
                reqs = requests.get(link, headers=headers, timeout=10)
                reqs.encoding = 'utf8'
                ht1 = etree.HTML(reqs.text)
                bt = ht1.xpath("//h1[@class='content_left_title']/text()")  # 标题
                if bt:
                    data.append([fl[n]])
                    data.append(ht1.xpath("//h1[@class='content_left_title']/text()"))  # 标题
                    data.append(ht1.xpath("//div[@class='left_zw']/p/text()"))  # 简介
                    data.append([links[n]])
                else:
                    data.append([fl[n]])
                    data.append(ht1.xpath("//div[@class='content_title']/div[@class='title']/text()"))
                    data.append(ht1.xpath("//div[@class='content_desc']/p/text()"))  # 简介
                    data.append([links[n]])
                text = ''
                for y in range(len(data) - 1):
                    text += ''.join(data[y])
                text = preprocess_text_zh(text)
                with open(out_path, "a", encoding="utf-8") as f:
                    json.dump({links[n]:text}, f, ensure_ascii=False)
                    f.write("\n")
                n += 1
            except Exception as arr:
                continue

 
 
if __name__ == '__main__':
    urls = cnew_url()
    print(urls)
    cnew_data(urls, out_path='data/news_zh.json')