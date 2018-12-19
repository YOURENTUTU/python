# coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import json
import time

stocklist=[]
alldata=[]
userdatalist=[]
numlist=[]
driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

def getHtml(url):
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    return soup

def finddata(soup):
    singledata = {}
    datadiv=soup.find("div",{"class":"qphox layout mb7 clearfix"})
    if(datadiv==None):
        datadiv=soup.find("div",{"class":"qphox layout mb7"})
        if(datadiv!=None):
            singledata= finddata2(datadiv,singledata)
        return singledata
    strong=datadiv.find("div",{"id":"arrowud"}).strong
    singledata["color"]=strong.attrs["class"][-1]
    singledata["number"]=strong.string
    ullist=datadiv.find_all("ul")
    for ul in ullist:
        lilist=ul.find_all("li")
        for li in lilist:
            singledata[li.span.string]=li.span.nextSibling.string
    return singledata

def finddata2(datadiv,singledata):
    strong=datadiv.find("strong",{"id":"price9"})
    singledata["color"] = strong.attrs["class"][-1]
    singledata["number"] = strong.string
    trlist=datadiv.find_all("tr")
    i=1
    for tr in trlist:
        tdlist=tr.find_all("td")
        for td in tdlist:
            if(td.attrs=={}):
                singledata[td.string]=tr.find("td",{"id":"gt"+str(i)}).string
                i = i + 1
    return singledata

def findlist():
    url="http://quote.eastmoney.com/stocklist.html"
    soup= getHtml(url)
    search= soup.find("div",{"id":"quotesearch"})
    ullist=search.find_all("ul")
    for ul in ullist:
        lilist= ul.find_all("li")
        for li in lilist:
            data = []
            a= li.find("a",{"target":"_blank"})
            data.append(a.string)
            data.append(a.attrs["href"])
            stocklist.append(data)

def getlist():
    with open("test2.txt","r") as f:
        for line in f:
            data = []
            data.append(line.split("(")[0])
            data.append(line.split(")")[1])
            stocklist.append(data)

def findurl(name):
    for data in stocklist:
        a= data[0].split("(")[0]
        if a==name:
            return data

def getalldata():
    for stock in stocklist:
        print(stock[0])
        soup = getHtml(stock[1])
        data = finddata(soup)
        real = {stock[0]: data}
        alldata.append(real)

def writedown():
    js = json.dumps(alldata, indent=4, ensure_ascii=False)
    with open("gp2.txt", "w", encoding="utf-8") as f:
        f.write(js)

def getuser():
    with open("user.txt","r",encoding="utf-8") as f:
        for line in f:
            userdatalist.append(line.replace("\n",""))

def query(user):
    stock = findurl(user)
    soup = getHtml(stock[1])
    data = finddata(soup)
    real = {stock[0]: data}
    alldata.append(real)
    return real

def display():
    for single in alldata:
        print(single)
    return

def writeuser(name):
    with open("user.txt", "r", encoding="utf-8") as f:
        for line in f:
            if(line.replace("\n","")==name):
                return
    with open("user.txt", "a", encoding="utf-8") as f:
        f.write(name + "\n")

def findnumber(soup):
    s=''
    datadiv = soup.find("div", {"class": "qphox layout mb7 clearfix"})
    if (datadiv == None):
        datadiv = soup.find("div", {"class": "qphox layout mb7"})
        if (datadiv != None):
            s= findnumber2(datadiv)
        return s
    strong = datadiv.find("div", {"id": "arrowud"}).strong
    return strong.string

def findnumber2(datadiv):
    strong = datadiv.find("strong", {"id": "price9"})
    return strong.string

def show():
    for stock in stocklist:
        soup = getHtml(stock[1])
        s= findnumber(soup)
        if s not in ["","-","已退市","终止上市","停牌","未上市","暂停上市"]:
            with open("numlist", "a") as f:
                    f.write(s+"\n")
            numlist.append(eval(s))
    plt.plot(numlist, 'k')
    plt.savefig("chart.png")
    plt.show()

def user():
    print("请选择你要进行的操作：")
    print("1.查询  2.显示您当前的股票信息 3.查看最近您股票的变化情况 4.退出")
    action=input(":")
    num=eval(action)
    if (num==1):
        name=input("请输入股票名称：")
        writeuser(name)
        print(query(name))
    elif(num==2):
        getuser()
        for user in userdatalist:
            query(user)
        display()
        writedown()
    elif(num==3):
        show()
    elif(num==4):
        return "quit"

def userControl():
    print("欢迎进入股票爬虫服务")
    flag=""
    while(flag!="quit"):
        flag=user()
    return

def main():
    #url='http://quote.eastmoney.com/sh512800.html'
    #findlist()
    getlist()
    userControl()
    #getalldata()
    #writedown()
    driver.close()
    print("结束")
    return

if __name__ == '__main__':
    main()