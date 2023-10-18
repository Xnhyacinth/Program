import requests
import re
import time

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


def spider_page(url):
	"""
	爬取某一页的数据
	:param url:
	:return:
	"""
	response = requests.get(url, headers=HEADERS)
	text_raw = response.text

	# print(text_raw)

	# 1.获取所有的标题
	titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>', text_raw, re.DOTALL)

	# 2.获取作者信息<p\sclass="source">.*?<a.*?><img.*?>(.*?)</a><a.*?>.*?</a>
	authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<img.*?>\n(.*?)</a>', text_raw, re.DOTALL)
	
	# 3.获取所有的朝代
	dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>', text_raw, re.DOTALL)

	# 4.获取古诗文内容
	# 内容待进一步美化【去掉多余的元素】
	contents_pre = re.findall(r'<div\sclass="contson".*?>(.*?)</div>', text_raw, re.DOTALL)

	contents = []
	for content_pre in contents_pre:
		# 4.1 利用sub()函数把内容中的【<.*?>或者换行字符】替换为空
		content = re.sub(r'<.*?>|\n', "", content_pre)
		contents.append(content.strip())

	# 诗词列表数据
	poems = []

	# 5. 使用zip()把四个列表组合在一起
	for value in zip(titles, dynasties, authors, contents):
		# 5.1 自动进行解包放入到变量当中
		title, dynastie, author, content = value

		# 5.2 新建dict，并加入到诗词列表数据中
		poem = {
			'title': title,
			'dynastie': dynastie,
			'author': author,
			'content': content
		}

		poems.append(poem)

	return poems


def spider():
	# 全部诗词列表数据
	poems = []

	page_num, n = 0, 0
	while page_num < 2 and n < 10:
		url = 'https://www.gushiwen.org/default_{}.aspx'.format(page_num + 1)

		print('开始爬取第{}页诗词数据'.format(page_num + 1))

		try:
			poems.append(spider_page(url))
		except:
			n += 1
			continue
		n = 0
		page_num += 1
		time.sleep(1)

	# 2.显示数据
	for poem in poems:
		print(poem)
		print("==" * 40)

	print('Finished!')


if __name__ == '__main__':
	spider()