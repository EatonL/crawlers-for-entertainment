import urllib.request
import urllib.parse
import re
import os
import importlib
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--word", type=str, default=None,
	help="secret word for searching")
args = vars(ap.parse_args())

importlib.reload(sys)

header=\
{
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
     "referer":"https://image.baidu.com"
    }

keyword=args["word"]
keyword=urllib.parse.quote(keyword,"utf-8")
n=0
j=0
error=0
while(n<30*100):
    url="https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn={pageNum}&rn=30&gsm=1e00000000001e&1490169411926="
    n+=30
    url1=url.format(word=keyword,pageNum=str(n))
 
    rep=urllib.request.Request(url1,headers=header)
    rep=urllib.request.urlopen(rep)
    try:
        html=rep.read().decode("utf-8")
    except:
        print("something wrong!")
        error=1
        print("-------------now page ="+str(n))
    if(error==1): 
        continue
    p=re.compile("thumbURL.*?\.jpg")
    s=p.findall(html)

    if os.path.isdir(r"./baidu_img")!=True:
        os.makedirs(r"./baidu_img")
    with open("testPic1.txt","w") as f:
        for i in s:
            i=i.replace("thumbURL\":\"","")
            print(i)
            f.write(i)
            f.write("\n")
            urllib.request.urlretrieve(i,"./baidu_img/pic{num}.jpg".format(num=j))
            j+=1