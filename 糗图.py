import urllib.request
import re
import os
import time


def generate_request(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	}
	request = urllib.request.Request(url=url, headers=headers)
	return request


def get_response(request):
	response = urllib.request.urlopen(request)
	return response.read().decode('utf8')


def parse_content(content):

	pattern = re.compile(r'<div class="thumb">.*?<img src="(.*?)" alt="(.*?)" />.*?</div>', re.S)
	ret = pattern.findall(content)

	down_load(ret)

def down_load(ret):
	dirname = 'qiutu'
	for tp in ret:

		image_src = 'https:' + tp[0]

		title = tp[1]

		filename = title + '.' + image_src.split('.')[-1]
		filepath = os.path.join(dirname, filename)
		print('正在下载图片%s...' % filename)
		urllib.request.urlretrieve(image_src, filepath)
		print('结束下载图片%s' % filename)
		time.sleep(2)

def main():

	start_page = int(input('请输入起始页码:'))

	end_page = int(input('请输入结束页码:'))
	url = 'https://www.qiushibaike.com/pic/page/'
	for page in range(start_page, end_page + 1):
		print('正在下载第%s页.........' % page)

		new_url = url + str(page) + '/'
		request = generate_request(new_url)

		content = get_response(request)

		parse_content(content)
		print('结束下载第%s页......' % page)
		time.sleep(2)

if __name__ == '__main__':
	main()