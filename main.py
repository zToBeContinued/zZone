from bs4 import BeautifulSoup #网页解析，获取数据
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url，获取网页数据
import xlwt  #进行excel操作
import time
import sqlite3  #进行sqline数据库操作

def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    #2.解析数据
    #3.保存数据
    saveData(datalist,savepath)

    # askURL("https://movie.douban.com/top250?start=0")

#影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  #创建正则表达式对象，表示规则（字符串的模式）
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S  让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
#影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)

        #2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",class_="item"): #查找符合要求的字符串，形成列表
            data = []
            item = str(item)

            #影片详情的超链接
            link = re.findall(findLink,item)[0]  #re库用来通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if len(titles) == 2:
                ctitle = titles[0]  #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/","")  #添加外国名
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')  #外国名留空
            
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq,item)
            if len(inq) != 0:
                inq = inq[0].replace('。','')
                data.append(inq)
            else:
                data.append(' ')
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s)?'," ",bd)  #去掉<br/>
            bd = re.sub('/',' ',bd)
            data.append(bd.strip())  #去掉前后的空格
            datalist.append(data)
        print("已完成"+str((i+1))+"页")
        time.sleep(1)
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
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
    

#保存数据
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)  #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概识","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,len(datalist)):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

if __name__ == "__main__":
    main() 
    print("爬取完毕！")