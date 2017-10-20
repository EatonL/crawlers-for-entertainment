import urllib2
import urllib
import re
from BeautifulSoup import BeautifulSoup

def getAllImageLink():
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    #req = urllib2.Request(url = 'http://music.163.com/#/discover/toplist',headers = headers)
    req = urllib2.Request(url = 'http://music.163.com/#/discover/toplist?id=3778678',headers = headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    #print(soup)
    title= soup.findAll("title")
    div1 = soup.findAll("div",{'id' : 'song-list-pre-cache'})
    #div2 = soup.findAll(id=re.compile("song-list-pre-cache$")) 
    #div3 = soup.findAll('div',id_='song-list-pre-cache') 
    print(title)
    print(div1)
    #print(div1)
    #print(div2)
    #print(div3)
if __name__ == '__main__':
    getAllImageLink()
    