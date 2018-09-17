import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

def parse_first_page(url):
    r = requests.get(url, headers=headers)
    # 生成soup对象
    soup = BeautifulSoup(r.text, 'lxml')
    # 所有以数字开头的a对象
    number_oa_list = soup.select('.bus_kt_r1 > a')
    # 所有以字母开头的a对象
    char_oa_list = soup.select('.bus_kt_r2 > a')
    all_oa_list = number_oa_list + char_oa_list
    # print(len(all_oa_list))
    all_href_list = []
    # 提取得到所有的链接
    for oa in all_oa_list:
        # 添加协议和主机，拼接完整的href
        href = url.rstrip('/') + oa['href']
        # 将href添加到指定的列表中
        all_href_list.append(href)
    return all_href_list

def parse_second_page(url, all_href_list, fp):
    # 遍历这个列表，依次向每个二级页面发送请求
    for href in all_href_list:
        r = requests.get(url=href, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        # 提取所有的详细公交的链接
        odiv = soup.find('div', id='con_site_1')
        # 查找这个div下面的所有的a链接
        oa_list = odiv.find_all('a')
        # 提取所有的a对象的href属性
        oa_href_list = []
        for oa in oa_list:
            href = url.rstrip('/') + oa['href']
            oa_href_list.append(href)
        
        # 向所有的三级页面发送请求，依次提取数据
        parse_third_page(oa_href_list, fp)
        # print(len(oa_href_list))
        # exit()
    
def parse_third_page(oa_href_list, fp):
    for href in oa_href_list:
        r = requests.get(url=href, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        # 获取线路名称
        route_name = soup.select('.bus_i_t1 > h1')[0].string
        print('正在抓取---%s---' % route_name)
        # 获取运行时间
        run_time = soup.select('.bus_i_content > .bus_i_t4')[0].string.lstrip('运行时间：')
        # 获取票价信息
        piao_info = soup.select('.bus_i_content > .bus_i_t4')[1].string.lstrip('票价信息：')
        # 公交公司
        bus_company = soup.select('.bus_i_content > .bus_i_t4 > a')[0].string
        # 上行总站数  正则提取数字
        up_total = soup.select('.bus_line_top > span')[0].string.strip('共站 ')
        # 获取上行总站牌
        up_div = soup.select('.bus_line_site')[0]
        up_oa_list = up_div.select('.bus_site_layer > div > a')
        up_name_list = []
        # 遍历，获取所有的名字
        for oa in up_oa_list:
            up_name_list.append(oa.string)
        
        try:
            # 下行总站数  正则提取数字
            down_total = soup.select('.bus_line_top > span')[1].string.strip('共站 ')
            # 获取下行总站牌
            down_div = soup.select('.bus_line_site')[1]
            down_oa_list = down_div.select('.bus_site_layer > div > a')
            down_name_list = []
            # 遍历，获取所有的名字
            for oa in down_oa_list:
                down_name_list.append(oa.string)
        except Exception as e:
            down_total = '没有下行'
            down_name_list = []
 

        # 保存到字典中
        item = {
            '线路名称': route_name,
            '运行时间': run_time,
            '票价信息': piao_info,
            '公交公司': bus_company,
            '上行总站数': up_total,
            '上行总站牌': up_name_list,
            '下行总站数': down_total,
            '下行总站牌': down_name_list,
        }
        string = json.dumps(item, ensure_ascii=False)
        fp.write(string + '\n')
        print('结束抓取---%s---' % route_name)
        # time.sleep(2)

def main():
    fp = open('西安公交.txt', 'w', encoding='utf8')
    url = 'http://xian.8684.cn/'
    # 处理一级页面，得到所有的数字-字母开头链接
    all_href_list = parse_first_page(url)
    # 处理所有的二级页面
    parse_second_page(url, all_href_list, fp)
    fp.close()

if __name__ == '__main__':
    main()