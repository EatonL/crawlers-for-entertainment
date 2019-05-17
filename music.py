import requests
import json
import time
import pandas as pd

class music(object):
    def __init__(self,url,file_name):
        self.url=url
        self.file_name=file_name
        self.headers = {'User-agent':  
                      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        self.music_name=[]
        self.artist_name=[]
        self.pic_url=[]

    def get_data(self):  
        s = requests.session() 
        s.keep_alive = False
        response = s.get(self.url, headers=self.headers)
        response.encoding = response.apparent_encoding
        data=json.loads(response.content,encoding='utf-8')
        for i in range(len(data['result']['tracks'])):
            self.music_name.append(data['result']['tracks'][i]['name'])
            self.artist_name.append(data['result']['tracks'][i]['artists'][0]['name'])
            self.pic_url.append(data['result']['tracks'][i]['album']['picUrl'])

    def extract(self):
        self.get_data()
        ticks = [time.ctime()]
        ticks = list(ticks)

        max_length = len(self.music_name)
        ticks.extend([""]*(max_length-len(ticks)))

        test = pd.DataFrame({'time':ticks,'music':self.music_name,'artist':self.artist_name,'pic':self.pic_url})
        print(test)
        path = './163music_'+self.file_name+str(ticks[0]).replace(':','-')+'.csv'
        test.to_csv(path,encoding='utf-8-sig',index=False)


def main():
    data=music("http://music.163.com/api/playlist/detail?id=2884035",'网易原创歌曲榜')
    data.extract()
    
    data=music("http://music.163.com/api/playlist/detail?id=19723756",'云音乐飙升榜')
    data.extract()
    
    data=music("http://music.163.com/api/playlist/detail?id=3778678",'云音乐热歌榜')
    data.extract()

    data=music("http://music.163.com/api/playlist/detail?id=3779629",'云音乐新歌榜')
    data.extract()    
if __name__ == '__main__':
    main()