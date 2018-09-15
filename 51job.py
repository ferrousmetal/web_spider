#-*- coding:utf-8 -*-
import urllib.request,urllib.parse

import time
from bs4 import BeautifulSoup

start_page=int(input("start:"))
end_page=int(input("end:"))

url="https://search.51job.com/list/200200,000000,0000,00,9,99,python,2,{}.html"

with open("job.txt","w",encoding="utf8") as f:
    for page in range(start_page,end_page+1):
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        new_url=url.format(page)
        print(new_url)
        request=urllib.request.Request(url=new_url,headers=headers)
        response=urllib.request.urlopen(request).read().decode('gbk')
        soup=BeautifulSoup(response,"lxml")
        first=soup.find('div',id="resultList")
        second=first.find_all("div",class_="el")[1:]

        for job in second:
            work=job.select('.t1 > span > a')[0]["title"]
            conmpany=job.select(".t2 a")[0]["title"]
            location=job.select(".t3")[0].string
            salary=job.select(".t4")[0].string
            job_dict = {
                "职位":work,
                "公司":conmpany,
                "公司地址":location,
                "薪资":salary,
                }
            f.write(str(job_dict)+"\n")
    time.sleep(3)

