#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from io import StringIO
from colorama import init
from colorama import Fore, Back, Style
import lxml.html
import time
import re
import requests
import argparse
import sys
import os
from datetime import datetime, date, timedelta
from time import strftime
from bs4 import BeautifulSoup
from random import shuffle, randint
import glob


FACEBOOK_URL = 'https://www.facebook.com'
GROUPS_ID_LIST = []

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'

def sleep_time(seconds, count_down_msg = 'YES'):
  while seconds >= 0:
    if count_down_msg == 'YES':
      print('count down = %04s' %seconds, end = '\r')
    time.sleep(1)
    seconds = seconds - 1
  if count_down_msg == 'YES':
    print(end = '\n')


def facebook_login(username,password):
  print ("\nLogin to Facebook...."),

  sys.stdout.flush() 
  url = "http://www.facebook.com"
  driver.get(url)
  elem = driver.find_element_by_id("email")
  elem.send_keys(username)
  elem = driver.find_element_by_id("pass")
  elem.send_keys(password)
  elem.send_keys(Keys.RETURN)
  sleep_time(1)
  html_source = driver.page_source
  if "Please re-enter your password" in html_source or "Incorrect Email" in html_source:
          print ("Incorrect Username or Password")
          driver.close()
          exit()
  else:
          print ("Success\n")
  return driver.get_cookies()

def facebook_logout():
  print ("\nLogout to Facebook...."),
  url = "http://www.facebook.com"
  driver.get(url)
  logoutMenu = driver.find_element_by_id("logoutMenu")
  logoutMenu.click()
  sleep_time(3, "N")
  # logoutBtn  = driver.find_element_by_xpath("//*[@action='https://www.facebook.com/logout.php']")
  logoutBtn  = driver.find_element_by_xpath("//*[text()='Log Out']")
  logoutBtn.click()
  print ("Logout Success\n")


def write_line_to_file(filename, line):
  f = open (filename, 'a', encoding = 'utf-8')
  f.write(line+'\n')
  f.close()


def facebook_collect_groups_id():
  print("collecting groups... wait a minutes")
  url = "https://www.facebook.com/groups/?category=membership"
  driver.get(url)

  GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")
  lenOfPage = facebook_scroll_end_of_page() 

  while(True):
    lastCount = lenOfPage
    # sleep_time(1, N)
    lenOfPage = facebook_scroll_end_of_page() 
    GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")
    if len(GroupsElemsList) > 200:
      break

    if lastCount == lenOfPage:
      break

  print("total %s groups" %(len(GroupsElemsList)))
  for group in GroupsElemsList:
    group_name = group.text
    group_link = group.get_attribute('href') 
    group_id   = group.get_attribute('data-hovercard').split('=')[1]
    GROUPS_ID_LIST.append({group_id:group_name})
    line = group_id + '=' + group_name
    write_line_to_file('groups.cfg', line) 

  #
  # Using BS4 to parser group html source
  #
  # html_source = driver.page_source
  # soup = BeautifulSoup(html_source, 'lxml')
  # for groups in soup.find_all('a', {'class':'groupsRecommendedTitle'}):
  #   group_name = groups.string
  #   group_link = groups.get('href')


def facebook_post_to_groups(GroupId, GroupName, TextMessage):
  url = FACEBOOK_URL + '/' + GroupId
  driver.get(url)
  sleep_time(4, count_down_msg = 'NO')
  
  try:
    TextAreaElem = driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
  except:
    print("%s %s on %s (%s) NoTextAreaElem" %(current_time(), TextMessage, GroupName, GroupId))
    return "NoTextAreaElem"

  sleep_time(3, count_down_msg = 'NO')
  try:
    TextAreaElem.send_keys(TextMessage)
    # driver.implicitly_wait(3) # seconds
  except:
    print("%s %s on %s (%s) send key failed" %(current_time(), TextMessage, GroupName, GroupId))
    return "SendKeyFailed"

  sleep_time(6, count_down_msg = 'NO')
  retry_count = 0
  while True:
    try:
      PostBtnElem = driver.find_element_by_xpath("//button/span[.='Post']").click()
      print("%s %s on %s (%s) successed" %(current_time(), TextMessage, GroupName, GroupId))
      break
    except:
      print("Post Button is not exist")
      retry_count = retry_count + 1
      sleep_time(1, 'NO')

      if retry_count == 5:
        return "NoPostBtnElem"
  
  return 0

  # PostBtnElem = driver.find_element_by_xpath("//button/span[.='Post']")
  # driver.implicitly_wait(3) # seconds
  # PostBtnElem.click()

def GetChromeOptions_Notification(Value):
  #
  # 1 = Allow notification , 2 = Block notification 
  #
  chrome_options = webdriver.ChromeOptions()
  prefs = {"profile.default_content_setting_values.notifications" : Value}
  chrome_options.add_experimental_option("prefs",prefs)
  # driver = webdriver.Chrome(chrome_options=chrome_options)
  return chrome_options


def facebook_get_graphic_token():
  url = 'https://www.facebook.com/v2.3/dialog/oauth?response_type=token&display=popup&client_id=145634995501895&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2Fcallback&scope=user_about_me%2Cuser_actions.books%2Cuser_actions.fitness%2Cuser_actions.music%2Cuser_actions.news%2Cuser_actions.video%2Cuser_birthday%2Cuser_education_history%2Cuser_events%2Cuser_friends%2Cuser_games_activity%2Cuser_hometown%2Cuser_likes%2Cuser_location%2Cuser_photos%2Cuser_posts%2Cuser_relationship_details%2Cuser_relationships%2Cuser_religion_politics%2Cuser_status%2Cuser_tagged_places%2Cuser_videos%2Cuser_website%2Cuser_work_history%2Cads_management%2Cads_read%2Cemail%2Cmanage_notifications%2Cmanage_pages%2Cpages_manage_leads%2Cpublish_actions%2Cpublish_pages%2Cread_custom_friendlists%2Cread_insights%2Cread_mailbox%2Cread_page_mailboxes%2Cread_stream%2Crsvp_event'
  driver.get(url)
  while True:
      try:
          OkayBtnElem = driver.find_element_by_name('__CONFIRM__').click()
          sleep_time(3)
      except:
          break
  html_source = driver.page_source
  access_token_start = html_source.find('"accessToken"')
  access_token = html_source[access_token_start:-1].split(',')[0].split(':')[1]
  return access_token


def facebook_scroll_end_of_page():
  lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  sleep_time(2)
  return lenOfPage
  # match=False
  # while(match==False):
  #   lastCount = lenOfPage
  #   time.sleep(1)
  #   lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  #   if lastCount == lenOfPage:
  #     match=True

def facebook_search_by_type(search_type, key_word):
  facebook_search_url = 'https://www.facebook.com/search/'
  url = facebook_search_url + search_type + '/?q=' + key_word 
  driver.get(url)
  lenOfPage = facebook_scroll_end_of_page()

  while True:
    lastCount = lenOfPage
    lenOfPage = facebook_scroll_end_of_page()
    driver.find_element_by_xpath

def get_message_from_file(message_file):
  if not (os.path.isfile(message_file) and os.access(message_file, os.R_OK)):
    print('%s is not exist' %message_file)
    exit();

  f = open(message_file, "r", encoding = 'utf-8')
  data = f.read()
  
  if len(data) == 0:
    print('%s is empty, please check it again' %message_file)
    exit();

  return data

def get_arctile_number_list():
  filelist = []
  fpath = "./arctile/*"
  filelist = glob.glob(fpath)
  return filelist


# if sys.platform != 'win32' and sys.platform != 'darwin':
#   from pyvirtualdisplay import Display

init(autoreset=True)

parser = argparse.ArgumentParser(usage="-h for full usage")
parser.add_argument('-username', dest="username", help='facebook username to login with (e.g. example@example.com)',required=True)
parser.add_argument('-password', dest="password", help='facebook password to login with (e.g. \'password\')',required=True)

args = parser.parse_args()

username = args.username
password = args.password

acrtile_path_list = get_arctile_number_list()
acrtile_path_list_len = len(acrtile_path_list)

# if sys.platform != 'win32' and sys.platform != 'darwin' :
#   display = Display(visible=0, size=(1600, 900))
#   display.start()

notifications_block = 2
ChromPrefs = GetChromeOptions_Notification(notifications_block)

if sys.platform == 'win32':
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=ChromPrefs)

if sys.platform == 'darwin':
    driver = webdriver.Chrome('./chromedriver', chrome_options=ChromPrefs)


cookies = dict()
cookies = facebook_login(username,password)

# read_message_from_file()
# facebook_get_graphic_token()
facebook_collect_groups_id()
# modify_group_list_file = input('Do you want to modify groups.cfg. Y or N : ')
# if modify_group_list_file == 'Y':
#   print("y")
# else:
#   print("n")


post_count = 0
process_start_time = datetime.now()
next_start_time = process_start_time + timedelta(seconds = 3600)

# for msg in msglist:
while True:
  for fb_group_dict in GROUPS_ID_LIST:
    for fb_group_id, fb_group_name in fb_group_dict.items():
      print('============== Start post ===============')
      shuffle(acrtile_path_list)
      rand_num = randint(0, acrtile_path_list_len - 1)
      arctile_path = acrtile_path_list[rand_num]
      msg = get_message_from_file(arctile_path)
      post_status = facebook_post_to_groups(fb_group_id, fb_group_name,  msg)

      # if post status failed, remove the gruoup from list.
      if (post_status == "SendKeyFailed"):
        break;

      if (post_status != 0):
        print("remove %s %s" %(fb_group_id, fb_group_name))
        GROUPS_ID_LIST.remove(fb_group_dict)
        break
        
      print('=============== End post ================\n')
      sleep_time(120)

      post_count += 1
      if (post_count % 10 == 0):
        print("%s already post %s articles, force to sleep 10 minutes\n" %(current_time(), post_count))
        sleep_time(600)

      process_start_time = datetime.now()
      if process_start_time >= next_start_time:
        next_start_time = process_start_time + timedelta(seconds = 3600)
        print("%s Sleeping....   next start time on %s" %(current_time(), next_start_time.strftime('%Y/%m/%d %H:%M:%S')))
        facebook_logout()
        sleep_time(3600)
        cookies = facebook_login(username,password)
        process_start_time = datetime.now()
        next_start_time = process_start_time + timedelta(seconds = 3600)


# driver.close()
exit()


