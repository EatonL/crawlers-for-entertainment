#coding:utf-8
import argparse
import schedule
import threading
import douban
import renren
import steam
import music

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--spider", type=str, default="renren",
	help="select a particular spider")
ap.add_argument("-t", "--time", type=float, default=24,
	help="determin a run cycle")  
args = vars(ap.parse_args())

def run():
    if args["spider"]=="douban":
        douban.main()
    elif args["spider"]=="renren":
        renren.main()
    elif args["spider"]=="steam":
        steam.main()
    elif args["spider"]=="163music":
        music.main()    
    elif args["spider"]=="all":
        threading.Thread(target=douban.main()).start()
        threading.Thread(target=renren.main()).start()
        threading.Thread(target=steam.main()).start()
        threading.Thread(target=music.main()).start()
def main():
    schedule.every(10*args["time"]).seconds.do(run)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()



