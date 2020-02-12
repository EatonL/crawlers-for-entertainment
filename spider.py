#coding:utf-8
import argparse
import schedule
import threading
from douban import douban
from renren import renren
#import bilibili
from steam import steam
from music import music
import os
from sendEmail import sendEmail

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--spider", type=str, default="renren",
	help="select a particular spider")
ap.add_argument("-t", "--time", type=float, default=24,
	help="determin a run cycle")
ap.add_argument("-m", "--mail", type=str, default="Y",
	help="send Email?")
args = vars(ap.parse_args())

def run():
    if args["spider"]=="douban":
        data=douban("https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=")
        filePath=data.extract()
        if args["mail"]=="Y":
            if os.path.isfile(filePath):
                Mail=sendEmail('xxxxx@qq.com','xxxxx@qq.com','xxxxx','smtp.qq.com',None,'ok',str(filePath))
                Mail.sendMail()
            else:
                print("%s does not exist!" % filePath)
    elif args["spider"]=="renren":
        data=renren("http://www.zmz2019.com/")
        filePath=data.extract()
        if args["mail"]=="Y":
            if os.path.isfile(filePath):
                Mail=sendEmail('xxxxx@qq.com','xxxxx@qq.com','xxxxx','smtp.qq.com',None,'ok',str(filePath))
                Mail.sendMail()
            else:
                print("%s does not exist!" % filePath)      
    elif args["spider"]=="steam":
        data1=steam("https://store.steampowered.com/search/?filter=globaltopsellers&page=",'steam_topseller_',discount=False)
        filePath1=data1.extract()
        print(filePath1)
        data2=steam("https://store.steampowered.com/search/?os=win&specials=1&page=",'steam_specials_',discount=True)
        filePath2=data2.extract()
        print(filePath2)
        if args["mail"]=="Y":
            if os.path.isfile(str(filePath1)):
                Mail=sendEmail('xxxxx@qq.com','xxxxx@qq.com','xxxxx','smtp.qq.com',None,'ok',str(filePath1),str(filePath2))
                Mail.sendMail()
            else:
                print("%s %s do not exist!" % (filePath1,filePath2))      
    elif args["spider"]=="163music":
        data=music("http://music.163.com/api/playlist/detail?id=2884035",'网易原创歌曲榜')
        filePath1=data.extract()
    
        data=music("http://music.163.com/api/playlist/detail?id=19723756",'云音乐飙升榜')
        filePath2=data.extract()
    
        data=music("http://music.163.com/api/playlist/detail?id=3778678",'云音乐热歌榜')
        filePath3=data.extract()

        data=music("http://music.163.com/api/playlist/detail?id=3779629",'云音乐新歌榜')
        filePath4=data.extract()
        if args["mail"]=="Y":
            if os.path.isfile(str(filePath1)) and os.path.isfile(str(filePath2)) and os.path.isfile(str(filePath3)) and os.path.isfile(str(filePath4)):
                Mail=sendEmail('xxxxx@qq.com','xxxxx@qq.com','xxxxx','smtp.qq.com',None,'ok',str(filePath1),str(filePath2),str(filePath3),str(filePath4))
                Mail.sendMail()
            else:
                print("%s %s %s %s do not exist!" % (filePath1,filePath2,str(filePath3),str(filePath4))) 
    #elif args["spider"]=="bilibili":
        #bilibili.main() 
    #elif args["spider"]=="all":
        #threading.Thread(target=douban.main()).start()
        #threading.Thread(target=renren.main()).start()
        #threading.Thread(target=steam.main()).start()
        #threading.Thread(target=music.main()).start()
        #threading.Thread(target=bilibili.main()).start()
def main():
    schedule.every(10*args["time"]).seconds.do(run)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()

