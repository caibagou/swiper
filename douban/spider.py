# -*- codeing = utf-8 -*-
# @Time : 2021/12/22 11:15
# @Author : tl
# @File : spider.py
# @Software : PyCharm

from bs4 import BeautifulSoup   #网页解析，获取数据
import re    #正则表达式，进行文字匹配
import urllib.request,urllib.error  #指定URL，获取网页数据
import xlwt   #进行excel操作
import sqlite3   #进行SQLite数据库操作


def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    #3.保存数据
    saveData(datalist,savepath)

#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     #生成正则表达式对象，表示规则（字符串的模式）
#影片图片的链接
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)        #.代表1个字符，*代表0到多个字符   re.S忽视换行符
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findIng = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)   #re.S忽视换行符 ?代表多次

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):    #调用获取页面信息的函数10次
        url = baseurl + str(i*25)
        html = askURL(url)
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = []    #保存一部电影的所有信息
            item = str(item)
            link = re.findall(findLink,item)[0]
            data.append(link)   #添加链接
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)     #添加图片

            titles = re.findall(findTitle,item)
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)     #添加中文名
                otitle = titles[1].replace('/','')      #去掉无关的符号
                data.append(otitle)     #添加外国名
            else:
                data.append(titles[0])
                data.append(' ')    #外国名留空

            rating = re.findall(findRating,item)[0]
            data.append(rating)     #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)       #添加评价人数

            inq = re.findall(findIng,item)
            if len(inq) !=0 :
                inq = inq[0].replace("。","")    #去掉句号
                data.append(inq)        #添加概述
            else:
                data.append(" ")    #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)     #去掉<br/>
            bd = re.sub('/'," ",bd)     #替换/
            data.append(bd.strip())     #去掉前后的空格

            datalist.append(data)      #把处理好的一部电影信息放入datalist

    print(datalist)
    return datalist



#得到指定一个URL的网页内容
def askURL(url):
    #模拟头部信息向服务器发送消息   用户代理，表示告诉豆办服务器，我们是什么类型的浏览器
    head = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0"}
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

#保存数据
def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)  #创建工作表
    col =("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])  #数据

    book.save(savepath)    #保存

if __name__ == "__main__":   #当程序执行时
    #调用函数
    main()
    print("爬取完毕！")