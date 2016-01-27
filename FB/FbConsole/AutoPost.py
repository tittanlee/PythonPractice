import fbconsole
import facebook
import requests
import os, sys
import os.path
import time
import datetime

GROUP_LIST_FILE_NAME = './groupset'
GroupList=[]

MESSAGE_FILE_NAME = './message'
MessageList=[]

GROUP_SLEEP_TIME = 60
TEXT_SLEEP_TIME  = 30

def GetGroupList():
  GroupFile = open(GROUP_LIST_FILE_NAME, 'r', encoding = 'utf-8')
  while True:
    GroupString = GroupFile.readline()
    if not GroupString:
      break
    else:
      # GroupId   = GroupString.split(',')[0]
      # GroupName = GroupString.split(',')[1]
      GroupList.append(GroupString)
  
  GroupFile.close()
  return 0

def GetMessageList():
  MsgFile = open(MESSAGE_FILE_NAME, 'r', encoding = 'utf-8')
  while True:
    MsgString = MsgFile.readline()
    if not MsgString:
      break
    else:
      MsgText   = MsgString.split(',')[0]
      MsgLink   = MsgString.split(',')[1]
      MessageList.append(MsgString.strip(' \r\n'))
      # print(MsgText)
      # print(MsgLink)
  
  MsgFile.close()
  return 0

def Countdown(count):
  while (count >= 0):
    print ('The count is: %03d' %(count), end='\r')
    count -= 1
    time.sleep(1)

def LogTheData(Content):
  LogFileName = datetime.datetime.now().strftime("%Y_%m%d") + '.log'
  LogFile = open(LogFileName, mode = 'a+', encoding = 'utf-8')
  LogTimeStamp = datetime.datetime.now().strftime("%Y_%m%d_%H:%M:%S")
  LogFile.write(LogTimeStamp + " >>> " + Content)
  LogFile.close()




if os.path.isfile(GROUP_LIST_FILE_NAME) and os.access(GROUP_LIST_FILE_NAME, os.R_OK):
  GetGroupList()
else:
  print('The gorupset file is not exist')
  sys.exit()


if os.path.isfile(MESSAGE_FILE_NAME) and os.access(MESSAGE_FILE_NAME, os.R_OK):
  GetMessageList()
else:
  print('The message file is not exist')
  sys.exit()


fbconsole.AUTH_SCOPE = ['publish_actions']
# fbconsole.APP_ID = '534039770107244'
# fbconsole.APP_ID = sys.argv[1]
TOKEN_FILE = '.fb_access_token'
fbconsole.authenticate()
access_token = fbconsole.ACCESS_TOKEN
access_token = 'CAACEdEose0cBAMdksmVnvBX4zZAX9alYey1dkwORQpsjRoInavY9athhPwOlQissv5EiqB1QSK6bzekTzZARd4WAsonqZAxoFQxBBlJ3kchOK8M5C0MhykEYVw18D0Ea2BYYtGoTHYQtXhGrk0YLFeHgKjnl3yoCsL6Cm5DPgJphnEcXNUycg1TzapZAFrLl3zjyvBAc9UyotIb2PnNQ'
graph = facebook.GraphAPI(access_token)


for Msg in MessageList:
  MsgText = Msg.split(',')[0]
  MsgLink = Msg.split(',')[1]
  # print(MsgText + MsgLink)
  for Group in GroupList:
    GroupId   = Group.split(',')[0].strip(' \r\n')
    GroupName = Group.split(',')[1].strip(' \r\n')
    LogData = ('Msg = %s, Link = %s, Id = %s, Name = %s' %(MsgText, MsgLink, GroupId, GroupName))
    try:
      # res = graph.put_wall_post(message=MsgText, attachment = {'link':MsgLink}, profile_id = GroupId )
      LogTheData(LogData+" OK\n")
    except:
      LogTheData(LogData+" ERROR\n")
    # Countdown(GROUP_SLEEP_TIME) 

  # Countdown(TEXT_SLEEP_TIME)


# fbconsole.AUTH_SCOPE = ['publish_actions', 'publish_checkins']
# fbconsole.APP_ID = '534039770107244'


# TOKEN_FILE = '.fb_access_token'
# fbconsole.authenticate()
# access_token = fbconsole.ACCESS_TOKEN


# graph = facebook.GraphAPI(access_token)
# me = graph.get_object('me')
# print(me)


# res = graph.put_wall_post(message="", attachment = {'link':'http://beefun01.com/p/2263/'}, profile_id = '670549976361152')
