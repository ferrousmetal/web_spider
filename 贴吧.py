import urllib.request,urllib.parse
import time
import os
url='http://tieba.baidu.com/f?'

kw=input("请输入要搜索的贴吧类型:")
ie="utf-8"
n1=int(input("起始页内容:"))
n2=int(input("终结页内容:"))

for page in range(n1,n2+1):
    pn=50*(page-1)

    data={
        "kw":kw,
        "ie":ie,
        "pn":str(pn),
    }

    new_url=url+urllib.parse.urlencode(data)

    headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    request=urllib.request.Request(url=new_url,headers=headers)

    response=urllib.request.urlopen(request)
    if not os.path.exists(kw):
        os.mkdir(kw)
    print("目录")
    filename="第%d页的内容"%page+".html"
    print("文件生成")

    filepath=os.path.join(kw,filename)

    with open (filepath,"wb") as f:
        f.write(response.read())
    print("下载完毕")
    time.sleep(3)