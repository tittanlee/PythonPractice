# -*- coding: <utf-8>-*-
import facebook
import requests


FACEBOOK_APP_ID  = "534039770107244"
FACEBOOK_APP_SECRET = "27b30f0ea6204f63feefd41efb8b384c"
FACEBOOK_PROFILE_ID = '752801398090343'


def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

# oauth_access_token = get_fb_token(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
# print(oauth_access_token)
Tittan_access_token = 'CAAHltNLLDWwBAAylRryl5MrdwX1QKSt1iJUZCqOUG1DkziQXCiBhDrqmMGYzDnSub0VawZAFhxe9hrCeq2MZCLj2iZBZABA3ypwcQIh5u8Mqo0JJaDE2JvQR3JvPX31TYhUWkHGqaDoazBel1i05GgvyuL1kiHx8Tcb0F5RI5u4E1RHcjkCI7viKPsZAaHOA0ZD'


graph = facebook.GraphAPI(Tittan_access_token, version='2.3')
me    = graph.get_object("me")
print(me)
# FbPersonalId = me['id']

groups = graph.get_object("me/groups")
print(groups)
# for GroupIdx in GroupsDict['data']:
  # print(GroupIdx['name'])
  # print(GroupIdx)

# group_id = groups['data'][6]['id'] # we take the ID of the first group
# print(groups['data'][6]['name'])
# print(group_id)


#
# ToDo post message , it is a list include dict{'message':'HERE_IS_YOUR_MSG','link':'YOUR_LINK_URL'}
# Data = [{'message':'HERE_IS_YOUR_MSG', 'link':'YOUR_LINK_URL'}]
#
# PostData = [{'message':'Great', 'link':'http://beefun01.com/p/1548/'}]
# graph.put_object(group_id, "feed", Data)
# graph.put_object(group_id, "feed", data = PostData)

# Likes = graph.get_object("me/likes")
# for LikeIdx in Likes['data']:
  # print(LikeIdx)



