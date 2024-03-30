#该程序的核心就是将Keyword拼接到url上，访问必应，处理返回的结果，所以如果某一天网
#站访问不了了或访问的url变了，那么这个程序就不能工作了

#程序用了requests和BeautifulSoup库

#外部py文件通过Key2result函数调用程序，返回的是列表类型
#如果成功，返回的列表包括 : 音标 and 释义
#列表索引[0]是音标(若没有音标该元素会为数字0)，后面的都是释义
#但是如果失败，返回的列表只有一个元素，为error字符串
import requests
from bs4 import BeautifulSoup


#获取要查询的单词，初始化url等信息，以字典返回
def InitInfo(keyword):
    keyword=keyword.replace(" ","")#keyword去空格
    u0="https://www.bing.com/dict/search?q="#必应翻译根路径
    dictInfo={
        "url":u0+keyword,
        "userAgent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36'
        }
    return dictInfo


#网络请求Get,成功则返回html文本，失败返回0
def GetHTML(dictInfo):
    head={"user-agent":dictInfo["userAgent"]}
    r=requests.request(method='get',url=dictInfo["url"],headers=head)
    if r.status_code==200:
        r.encoding=r.apparent_encoding
        return r.text
    else:
        return 0


#返回BeautifulSoup对象
def MakeSoup(raw):
    soup=BeautifulSoup(raw,'html.parser')
    return soup


#对BeautifulSoup对象的处理，返回结果的列表类型,失败返回0
#该函数的操作是基于必应网站的HTML的，如果网站HTML变动那么将不再适用
def Soup2result(soup):
    listResult=[]
    #英标
    hd_us=soup.find("div",{"class":"hd_prUS b_primtxt"})
    hd=soup.find("div",{"class":"hd_pr b_primtxt"})
    if hd_us==None or hd==None:
        listResult.append([0])
    else:
        listResult.append([hd_us.string,hd.string])
    #中文意思
    qdef=soup.find("div",{"class":"qdef"})
    if qdef==None:
        return 0
    ul=qdef.find("ul")
    if ul==None:
        return 0
    lis=ul.find_all("li")
    for li in lis:
        attr=li.span.string
        meaning=li.find_all("span")[1].find("span").string
        listResult.append([attr,meaning])
    return listResult


#此函数作为接口便于其他py文件调用，一步到位返回结果
#返回结果的列表类型
#网络错误返回["Internet Error:status_code"]或["Internet Error:find_error"]
def Key2result(keyword):
    dictInfo=InitInfo(keyword)
    raw=GetHTML(dictInfo)
    if raw==0:
        return ["Internet Error:status_code"]
    else:
        soup=MakeSoup(raw)
        result=Soup2result(soup)
        if result==0:
            return ["Internet Error:find_error"]
        else:
            return result



if __name__=='__main__':
    dictInfo=InitInfo("yes")
    raw=GetHTML(dictInfo)
    if raw==0:
        print(["Internet Error:status_code"])
    else:
        soup=MakeSoup(raw)
        result=Soup2result(soup)
        if result==0:
            print(["Internet Error:find_error"])
        else:
            print(result)
    
    
