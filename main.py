import time
from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
import json
import sender


# 讀取webhook資料
webhooklist=open("webhook.json","r")
webhooklist=json.load(webhooklist)
# 讀取時間資料
timelist=open("time.json","r")
timelist=json.load(timelist)

# 製作下一次通知時間
# 若今天已經過了發送時間，則明天再發
# 若今天還沒過發送時間，則今天還可以發送
nwtc=dt.now()
#print(nwtc)
eracelst=[]
for i in range(len(timelist)):
	timelist[i]["dttime"]=dt(#  最後一次傳送時間
		year=timelist[i]["time"]["Y"],
		month=timelist[i]["time"]["M"],
		day=timelist[i]["time"]["D"],
		hour=timelist[i]["sendtime"]["h"],
		minute=timelist[i]["sendtime"]["m"],
		second=timelist[i]["sendtime"]["s"]
	)
	timelist[i]["contest"]=dt(#  活動時間
		year=timelist[i]["time"]["Y"],
		month=timelist[i]["time"]["M"],
		day=timelist[i]["time"]["D"],
		hour=timelist[i]["time"]["h"],
		minute=timelist[i]["time"]["m"],
		second=timelist[i]["time"]["s"]
	)
	if(timelist[i]["contest"]<timelist[i]["dttime"]):#  最後一次傳送時間必須早於活動時間
		timelist[i]["dttime"]-=td(days=1)
	if(nwtc>timelist[i]["contest"]):#  contest已經結束
		eracelst.append(i)
	else:
		cton=timelist[i]["dttime"]-nwtc#  距離contest開始還有多久
		std=td(days=timelist[i]["sendafterD"])#  要過幾天才傳一次
		ct=int(cton/std)
		timelist[i]["nxt"]=timelist[i]["dttime"]-std*ct
	del timelist[i]["time"]
	del timelist[i]["sendtime"]
	timelist[i]["sendafterD"]=td(days=timelist[i]["sendafterD"])

eracelst.reverse()
for i in eracelst:
	timelist.pop(i)

eracelst=[]





firsttime=False#  測試用，第一次執行時會強制發送所有倒數訊息

try:
	while 1:
		print("\033[K", end="\r")
		nwtc=dt.now()
		eracelst=[]
		for i in range(len(timelist)):
			if(nwtc>timelist[i]["nxt"] or firsttime):#  發送
				#left=timelist[i]["contest"]-timelist[i]["nxt"]
				left=timelist[i]["contest"]-nwtc
				print(timelist[i]["title"],"剩下",left.days,"天\n已發送給", end="")
				for j in timelist[i]["sendto"]:
					if(webhooklist[j]["type"]=="dc"):
						sender.send_DC(webhooklist[j]["url"],timelist[i]["title"],left.days,left.seconds//3600,left.seconds//60%60)
						print(j,end=",")
				print()
				if(nwtc>timelist[i]["nxt"]):
					timelist[i]["nxt"]+=timelist[i]["sendafterD"]
				if(timelist[i]["nxt"]>timelist[i]["dttime"]):
					eracelst.append(i)
					print(timelist[i]["title"],"倒數結束，將不再發送倒數訊息")
				else:
					print("下次發送：",timelist[i]["nxt"])
		eracelst.reverse()
		for i in eracelst:
			timelist.pop(i)
		print(time.ctime(time.time()),"通知數量",len(timelist), end="\r")
		firsttime=False
		sleep(1)
except KeyboardInterrupt:
	print("\033[K", end="\r")
	print("程式由使用者強制中斷")
except:
	print("\033[K", end="\r")
	print("不明原因導致程式中斷")


