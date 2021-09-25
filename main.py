from bs4 import BeautifulSoup #网页解析，获取数据
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url，获取网页数据
import xlwt  #进行excel操作
import sqlite3  #进行sqline数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    #2.解析数据
    #3.保存数据

    # askURL("https://movie.douban.com/top250?start=0")

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)

        #2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all() #查找符合要求的字符串，形成列表
    return datalist

#得到指定一个url的网页内容
def askURL(url):
    head = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        respose = urllib.request.urlopen(request)
        html = respose.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
    

#保存数据
def saveData(savepath):
    print("save....")

if __name__ == "__main__":
    main() 