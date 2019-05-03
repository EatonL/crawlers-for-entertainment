import requests
import json
import time
import pandas as pd


headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0','Connection':'close'}


page=0
url=[]
movie_title=[]
movie_rate=[]

while True:
    requests.adapters.DEFAULT_RETRIES = 15
    s = requests.session()
    s.keep_alive = False
    
    url_visit = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start={}'.format(page*20)
    file = requests.get(url_visit,headers=headers).json()
    time.sleep(3)

    page+=1
    item_num=len(file['subjects'])
    if item_num<20:
        break
    for i in range(item_num):
        dict=file['subjects'][i]   
        urlname=dict['url']
        url.append(urlname)
        title=dict['title']
        movie_title.append(title)
        rate=dict['rate']
        movie_rate.append(rate)

ticks = [time.time()]
ticks = list(ticks)
ticks.extend([""]*(len(url)-len(ticks)))

test = pd.DataFrame({'time':ticks,'title':movie_title,'rate':movie_rate,'url':url})
path = './douban_'+str(ticks[0])+'.csv'
test.to_csv(path,encoding='utf-8-sig',index=False)      
        
print(movie_title)

