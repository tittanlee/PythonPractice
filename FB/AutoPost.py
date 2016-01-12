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
Tittan_access_token = 'CAACEdEose0cBAPqFvQvxRN3ZAJ9e7AgXCYsMG5hWqS7pgPdhR0OuadySdwimBWezSyVICpMJNOpug6arZCdnxCy0liaPlqw3hmQrryOSid6vZCCdsGb0MPZBZCZCJwopnCyKDpDQasRKE6S4nrwYpva9CzDCQtORKhZCrY0T88ZCiaQpnMVB0kYmWLbWAFPigWpj2PNcQIZCzz9RU98QbXfmF'

oauth_access_token = 'CAACEdEose0cBAIaMVM8MLdFE05cMZB6RC0S6Y0f0FZCX3O0I87I8erKc9L7KqWJK3xdEuhOOzAfKlsxrFmWulSpKLzNBdnV9D6N7KhsilSmZCZAwtMb488sWmWPJxmghpAR3QaYbUmi7nGmwJ3dSxXoekyPipsjNeENoQfXZCpUPPNLC8jZCQiCJKOCkksmhwAab308fmJKiDPRvZClzsGS'


graph = facebook.GraphAPI(Tittan_access_token, version='2.3')
me    = graph.get_object("me")
FbPersonalId = me['id']

GroupsDict= graph.get_object("me/groups")
for GroupIdx in GroupsDict['data']:
  print((GroupIdx['name'].decode('utf-8')))
  # print(GroupIdx)

# Likes = graph.get_object("me/likes")
# for LikeIdx in Likes['data']:
  # print(LikeIdx)

# group_id = groups['data'][0]['id'] # we take the ID of the first group
# print(group_id)


