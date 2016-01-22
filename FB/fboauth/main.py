import fbauth
import facebook


CLIENT_ID      = '534039770107244'
CLIENT_SECRETS = '27b30f0ea6204f63feefd41efb8b384c'

fbAuth = fbauth.TokenHandler(CLIENT_ID, CLIENT_SECRETS)
access_token = fbAuth.get_access_token()

graph = facebook.GraphAPI(access_token, version='2.3')

me = graph.get_object('me')

permissions = graph.get_object('me/permissions')
print(permissions)

version = graph.get_version()
print(version)

# SearchRes = graph.request('search', {'q':'free', 'type':'group'})
# print(SearchRes)

graph.put_object('me', 'feed', message = 'test')

# res = graph.put_wall_post(message="test", attachment = {'link':'http://beefun01.com/p/2263/'}, profile_id = '1444846532463984')
# print(res)
