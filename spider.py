#coding:utf-8

import argparse
import os
import timer
import sys
from apscheduler.schedulers.blocking import BlockingScheduler

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--spider", type=str, default="renren",
	help="select a particular spider")
ap.add_argument("-t", "--time", type=float, default=24,
	help="determin a run cycle")
ap.add_argument("-w", "--word", type=str, default=None,
	help="secret word for searching")   
args = vars(ap.parse_args())

spider_list = os.listdir(os.getcwd())

def run():
    if args["spider"]=="douban":
        os.system("python douban.py")
    elif args["spider"]=="renren":
        os.system("python renren.py")
    elif args["spider"]=="steam":
        os.system("python steam.py")
    elif args["spider"]=="baidu_img":
        os.system("python baidu_img.py -w {}".format(args["word"]))
    elif args["spider"]=="all":
        for c in spider_list:
            if os.path.isfile(c) and c.endswith('.py') and c.find("spider")== -1 and c.find("baidu_img") == -1: 
                os.system('python {}'.format(c))
        

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(run, 'interval', seconds=args["time"],id='spider_job')
    scheduler.start()

if __name__ == '__main__':
    main()



