from discord import SyncWebhook
import requests
import json





def send_DC(hook,title,d,h,m):
	data={
		"embeds":[
			{
				"title":title,
				"description":("剩下 "+str(d)+" 天 "+str(h)+" 時 "+str(m)+" 分"),
				"color":16711680
			}
		],
		"username":"小ㄌㄌ",
		"avatar_url":"https://avatars.githubusercontent.com/u/66681962",
		"attachments":[]
	}
	r=requests.post(hook,json.dumps(data),headers={'Content-Type':'application/json'})


	

if __name__ == '__main__':
	hook="<webhook here>"
	send_DC(hook,"學測倒數",10)
