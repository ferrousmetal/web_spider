import urllib.request
from bs4 import BeautifulSoup
import time

def gou_request(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}
	request = urllib.request.Request(url=url, headers=headers)
	return request

def get_text(href):
	# 构建请求对象
	request = gou_request(href)
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf8')
	# 生成soup对象
	soup = BeautifulSoup(content, 'lxml')
	# 首先找到内容div
	odiv = soup.find('div', class_='chapter_content')
	return odiv.text

def parse_content(content):
	# 生成哪个soup对象
	soup = BeautifulSoup(content, 'lxml')
	# 根据方法找所有的章节标题和链接
	oa_list = soup.select('.book-mulu a')
	# print(len(oa_list))
	# 遍历这个列表，得到每一个a对象的标题和链接
	fp = open('三国演义.txt', 'w', encoding='utf8')
	for oa in oa_list:
		# 得到标题
		title = oa.string
		print('正在下载---%s......' % title)
		# 得到链接
		href = 'http://www.shicimingju.com' + oa['href']
		# 向href发送请求，解析响应，得到这个章节的内容
		text = get_text(href)
		# 写入文件
		fp.write(title + '\n' + text)
		print('结束下载---%s...' % title)
		time.sleep(2)
	fp.close()

def main():
	url = 'http://www.shicimingju.com/book/sanguoyanyi.html'
	# 构建请求对象
	request = gou_request(url)
	# 发送请求。得到响应内容
	response = urllib.request.urlopen(request)
	content = response.read().decode('utf8')
	# 通过bs4解析这个网页内容
	parse_content(content)

if __name__ == '__main__':
	main()