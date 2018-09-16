import urllib.request,json,time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url="https://rate.tmall.com/list_detail_rate.htm?itemId=564620757154&spuId=473630836&sellerId=3634275930&order=3&currentPage={}"

header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
start_page=int(input('起始页:'))
end_page=int(input('结束页:'))

with open("评论.txt","w") as f:

    for page in range(start_page,end_page+1):
        new_url=url.format(page)

        request=urllib.request.Request(url=new_url,headers=header)
        content=urllib.request.urlopen(request).read().decode("utf8")
        comments=content.strip("jsonp128()\t\n\r")
        comment=json.loads(comments)
        for i in comment['rateDetail']['rateList']:
            neirong=i['rateContent']
            date=i["rateDate"]
            picture=i['pics']
            comment_user=i['displayUserNick']
            color_category=i['auctionSku']
            new_dict={
                '评论人':comment_user,
                '评论时间':date,
                '买家图':picture,
                '购买型号':color_category,
                '评价':neirong,
            }
            f.write(str(new_dict)+"\n")

    time.sleep(2)
    f.close()

