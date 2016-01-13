# -*- coding: <utf-8>-*-
import facebook
import requests


FACEBOOK_APP_ID = '963642153728423'
FACEBOOK_APP_SECRET = '063a6e06583189615f1314f8274f9e75'
FACEBOOK_PROFILE_ID = '752801398090343'

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

# oauth_access_token = get_fb_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
Tittan_access_token = 'CAACEdEose0cBAL7a4YrYHT5IpSHKoPpvT4eLayPxwYOSn5BIfja0kEd3ACdfzt7riZCqcHL71DT6OzuptIkAhIZCGczKvOjXFSg1qnqukRt2ELhm4MhIdXWmeGrmQkC3M3q3MQsvmLSB8V1TB1JFLZBO95oMZCqpkbGPxpX9PsE9io0tmGBYulmj35FKkqg54PbebNaW3X1sbZAVpyOh9'

graph = facebook.GraphAPI(Tittan_access_token, version='2.3')
me    = graph.get_object("me")
FbPersonalId = me['id']

groups = graph.get_object("me/groups")
# for GroupIdx in GroupsDict['data']:
  # print(GroupIdx['name'])
  # print(GroupIdx)

group_id = groups['data'][6]['id'] # we take the ID of the first group
print(groups['data'][6]['name'])
print(group_id)


#
# ToDo post message , it is a list include dict{'message':'HERE_IS_YOUR_MSG','link':'YOUR_LINK_URL'}
# Data = [{'message':'HERE_IS_YOUR_MSG', 'link':'YOUR_LINK_URL'}]
#
PostData = [{'message':'Great', 'link':'http://beefun01.com/p/1548/'}]
# graph.put_object(group_id, "feed", Data)
graph.put_object(group_id, "feed", data = PostData)

# Likes = graph.get_object("me/likes")
# for LikeIdx in Likes['data']:
  # print(LikeIdx)



