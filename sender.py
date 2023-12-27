from discord import SyncWebhook
import requests
import json





def send_DC(hook,title,days):
	data={
		"embeds":[
			{
				"title":title,
				"description":("剩下 "+str(days)+" 天"),
				"color":16711680
			}
		],
		"username":"小ㄌㄌ",
		"avatar_url":"https://avatars.githubusercontent.com/u/66681962",
		"attachments":[]
	}
	r=requests.post(hook,json.dumps(data),headers={'Content-Type':'application/json'})


	

if __name__ == '__main__':
	hook="https://ptb.discord.com/api/webhooks/1188864223841894470/AeclofLMywnP3vxd-q4RJpRvYFYUhLz5ZSOJoWxYq9VxuHi8auzqG9zmGAjOaZAPJ6sN"
	send_DC(hook,"學測倒數",10)