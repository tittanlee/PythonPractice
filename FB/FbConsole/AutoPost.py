import fbconsole
import facebook
import requests

fbconsole.AUTH_SCOPE = ['publish_actions', 'publish_checkins']
fbconsole.APP_ID = '534039770107244'



fbconsole.authenticate()
access_token = fbconsole.ACCESS_TOKEN


graph = facebook.GraphAPI(access_token)
me = graph.get_object('me')
print(me)


# res = graph.put_wall_post(message="", attachment = {'link':'http://beefun01.com/p/2263/'}, profile_id = '670549976361152')
