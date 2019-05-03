import urllib
from urllib import request 
import re  
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler


 
headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
url="http://www.zmz2019.com/"
#url = "http://www.zimuzu.io/"  the original website 

def get_article_url():   
    response = request.Request(url, headers=headers)
    html = request.urlopen(response)
    result = html.read().decode('utf-8')

    a = BeautifulSoup(result,"lxml")
    find_top24 = a.find_all('div',class_='fl box top24')  
    find_todayPlay = a.find_all("div",class_="fr today-play")
    
    return find_top24, find_todayPlay

def clean_data(data):
    data = str(data)
    pattern1 = re.compile(r'<a\b[^>]+\bhref="([^"]*)"[^>]*>',re.M)
    pattern2 = re.compile(r'<a\b[^>]+\btitle="([^"]*)"[^>]*>',re.M)
    data_href = [url[:-1]+x for x in pattern1.findall(data)]
    data_title = pattern2.findall(data)

    for x in range(len(data_href)-1,-1,-1):
        result = '/resource/' in data_href[x]        
        if result == False:
            data_href.remove(data_href[x])
        elif result == True:
            pass

    return data_href, data_title

def extract(data1=None,data2=None,data3=None,data4=None):
    ticks = [time.time()]
    ticks = list(ticks)

    max_length = len(data1) if len(data1)>len(data3) else len(data3)

    data1.extend([""]*(max_length-len(data1)))
    data2.extend([""]*(max_length-len(data2)))
    data3.extend([""]*(max_length-len(data3)))
    data4.extend([""]*(max_length-len(data4)))
    ticks.extend([""]*(max_length-len(ticks)))

    test = pd.DataFrame({'time':ticks,'top24_title':data1,'top24_href':data2,'todayplay_title':data3,'today_href':data4})
    print(test)
    path = './renren_'+str(ticks[0])+'.csv'
    test.to_csv(path,encoding='utf-8-sig',index=False)


def main():
    top24,todayPlay = get_article_url()
    top24_href,top24_title = clean_data(top24)
    del top24_href[0]
    todayplay_href, todayplay_title = clean_data(todayPlay)
  
    extract(top24_title,top24_href,todayplay_title,todayplay_href)

if __name__ == '__main__':
    main()
    #scheduler = BlockingScheduler()
    #scheduler.add_job(main, 'interval', seconds=30)
    #scheduler.start()


 



