# crawlers for entertainment

>一个致力于收集包括音乐榜单、游戏资讯、赛事资讯、电影榜单、美剧榜单等信息的娱乐向爬虫包

目前在学习python，于是练手之余写了这个demo，目前是初代，代码和功能都比较粗糙。

## 使用方法

```
python spider.py -s "name" -t "time" (-w "secret word")
```


**name:** 选用的爬虫名称，目前包括 baidu_img、renren、douban、steam、all（all是除了baidu_img的其他所有爬虫）

**time:** 爬虫的运行周期

**secret word:** 百度图片爬虫的搜索关键词，除了使用baidu_img时不用填。

所需模块：
urlib、re、os、impolib、sys、argparse、requests、json、time、pandas、beautifulsoup、apsheduler

所需环境：
python3.7, windows（linux系统还未测试，应该不会有什么大问题）

## 功能介绍

- 爬取steam热门游戏及特卖优惠游戏、豆瓣最近热门游戏、爬取人人影视热门美剧及美剧更新，以及根据关键词下载百度图片
- 定时爬取功能
- 将各类资讯分门别类存入csv文件，并以时间和类别命名

目标网络链接：

[https://image.baidu.com](https://image.baidu.com)

[https://movie.douban.com](https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0)

[http://www.zmz2019.com](http://www.zmz2019.com)

[https://store.steampowered.com(热卖)](https://store.steampowered.com/search/?filter=globaltopsellers&page=1)

[https://store.steampowered.com(优惠)](https://store.steampowered.com/search/?os=win&specials=1&page=1)

To do:

- 完成音乐榜单、赛事资讯爬取
- 统一各爬虫风格
- 重构定时功能（放弃apsheduler，自己写一个），采用线程分配
- 打包成exe程序，或者写个小网页显示
- 异常时采用代理IP或者cookies（豆瓣会阻止异常IP访问）
- 采用类的调用，不使用os.system调用各爬虫
- 写一个跨模块变量共享模块，方便存各模块参数


**后记：** 一方面由于入手爬虫时间不长，另一方面一直也是写写停停，到最后才决定汇总，所以问题挺多，包括：各个爬虫风格乱，request 和 urlib 都在用；有的模块封装了，有的模块还没封装；定时功能图省事用了现成模块，感觉更费事，而且不是多线程......导致最后主文件只能用 os.system 调用其他模块，而且调用模块太多，不方便打包，非常挺不 pythonic 。不过万事开头难，后面我会按计划慢慢补上。