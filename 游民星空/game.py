from selenium import webdriver
from BeautifulSoup import BeautifulSoup

driver = webdriver.PhantomJS("G:/phantomjs/bin/phantomjs.exe")
driver.get("http://www.gamersky.com/top")
soup = BeautifulSoup(driver.page_source)
title = soup.find(attrs={"class": "MpicY"}).findAll(attrs={"class": "tit"})
num = soup.find(attrs={"class": "MpicY"}).findAll(attrs={"class": "num"})
txt = soup.find(attrs={"class": "MpicY"}).findAll(attrs={"class": "txt"})
href = soup.find(attrs={"class": "MpicY"}).findAll(attrs={"target": "_blank"})
img = soup.find(attrs={"class": "MpicY"}).findAll(attrs={"width": "135"})
biaoge = soup.find(attrs={"class": "MpicY"})
print txt[0].text
#print href
#print(biaoge)
#print(title)
#print(num)