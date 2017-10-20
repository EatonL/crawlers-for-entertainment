from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib
import requests
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)# 禁用安全请求警告
post_param = {'action':'','start':'0','limit':'1'}
return_data = requests.get("https://movie.douban.com/ithil_j/activity/movie_annual2016/widget/1",data =post_param, verify = False)
json = return_data.json()
res = json['res']
sub = res['subjects']
for index in range(len(sub)):
    print sub[index]['title']
    print sub[index]['rating']
    print sub[index]['url']
    link = sub[index]['cover']
    filesavepath = '/Users/Messi/Desktop/python/%s.jpg' % index
    urllib.urlretrieve(link,filesavepath) 