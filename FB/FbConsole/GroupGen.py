import fbconsole
import facebook
import requests
import time



def countdown(count):
  while (count >= 0):
    print ('The count is: ', count)
    count -= 1
    time.sleep(1)
  print ("To Post Next\n")


# access_token = input('input token:')
access_token = 'CAACEdEose0cBAHYLVlUjf2gXo64oJcyN8gMqaluYJJETAKSjy7s4Gg9ac9gZBLfSZAKR8sTRVJU4UoMrLc1fJsuFq8ZAyHPQYe9elzO57xZAT1Sboa5be8Bc9b0PLhR4zZA2Q1XSm2Vz80Nmj3pqS8E2uioHrkrOh4JYYNZCqtVhbcT43JUZC86ZAt5EJXcjvv6OnaprKeCynCv1RrEWDPGQ'


def GroupGenerator():
  file = open('groupset', mode = 'w', encoding = 'utf-8')
  GroupCount = 0
  GroupSet = graph.get_object('me/groups')
  for group in fbconsole.iter_pages(GroupSet):
    GroupPrivacy = group['privacy']
    GroupId = group['id']
    GroupName = group['name']
    line = (GroupId + ":" + GroupName + "\n")
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

