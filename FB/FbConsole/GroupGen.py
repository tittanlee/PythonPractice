import fbconsole
import facebook
# import requests
# import time



def countdown(count):
  while (count >= 0):
    print ('The count is: ', count)
    count -= 1
    time.sleep(1)
  print ("To Post Next\n")


GRAPH_API_EXPLORER_URL = 'https://www.facebook.com/v2.3/dialog/oauth?response_type=token&display=popup&client_id=145634995501895&redirect_uri=https://developers.facebook.com/tools/explorer/callback#&scope=user_groups#'

print('Open your web browser then enter this URL:\n\n\n' + (GRAPH_API_EXPLORER_URL)) 

access_token = input('\n\nAccess Token=')
# access_token = 'CAACEdEose0cBAKx3VZCeyH6To5whD7sOYZBzeeH1abhaCMUl0yYSDY4C4NWo8Q8kn2IJ3sO6QTprFvwt6EeE5hxEPHsjiMIpDnhgYi3ZCFtxZC5fsuiIcpz9u7LQBLWnAL9aocdmaDz1N0ymgs3zyNROC7oX67PbZByGsxD7kYojqn6HF2c086yecl2yuIk4qWtoR8vjnLbsLQWjZAO9SH'

def GroupGenerator():
  file = open('groupset', mode = 'w', encoding = 'utf-8')
  GroupCount = 0
  GroupSet = graph.get_object('me/groups')
  for group in fbconsole.iter_pages(GroupSet):
    GroupPrivacy = group['privacy']
    GroupId = group['id']
    GroupName = group['name']
    # print(GroupId + " , " + GroupName)

    line = (GroupId + "," + GroupName + "\n")
    GroupCount += 1
    file.write(line)

  print("total %s groups be generated\n" %(GroupCount))
  file.close()

graph = facebook.GraphAPI(access_token, version='2.3')
GroupGenerator()

# GroupSet = graph.get_object('me/groups')
# for group in fbconsole.iter_pages(GroupSet):
#   if group['privacy'] == 'OPEN':
#     GroupId = group['id']
#     GroupName = group['name']
    # print('http://beefun01.com/p/2281/ post to ' + GroupName + ' ' +GroupId)
    # graph.put_wall_post(message="", attachment = {'link':'http://beefun01.com/p/2280/'}, profile_id = GroupId)
    # print(group)
    # countdown(5)

# res = graph.put_wall_post(message="", attachment = {'link':'http://beefun01.com/p/2282/'}, profile_id = '670549976361152')

