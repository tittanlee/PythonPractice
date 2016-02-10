#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from io import StringIO
import time
import re
import requests
import sys
import os
from datetime import datetime, date, timedelta
from time import strftime
from bs4 import BeautifulSoup
from random import shuffle, randint
import glob
import clipboard


FACEBOOK_URL = 'https://www.facebook.com'

def current_time():
  return '[' + (datetime.now()).strftime('%Y/%m/%d %H:%M:%S') + ']'

def sleep_time(seconds, count_down_msg = 'YES'):
  while seconds >= 0:
    if count_down_msg == 'YES':
      print('Count down = %04s' %(seconds), end = '\r')
    time.sleep(1)
    seconds = seconds - 1

  if count_down_msg == 'YES':
    print(end = '\n')

def rand_sleep_time(rand_start, rand_end, count_down_msg = 'YES'):
  rand_num = randint(rand_start, rand_end)
  sleep_time(rand_num, count_down_msg)

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
  GROUPS_FLIE_NAME = './groups.cfg'
  GROUPS_ID_LIST = list()

  if (os.path.isfile(GROUPS_FLIE_NAME) and os.access(GROUPS_FLIE_NAME, os.R_OK)):
      os.remove(GROUPS_FLIE_NAME)
  
  print("Collecting groups... wait a minutes...")
  url = "https://www.facebook.com/groups/?category=membership"
  driver.get(url)

  # GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")
  lenOfPage = facebook_scroll_end_of_page() 

  while(True):
    lastCount = lenOfPage
    lenOfPage = facebook_scroll_end_of_page() 
    GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")
    # Default maxime groups counts is 200
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
    write_line_to_file(GROUPS_FLIE_NAME, line) 
  
  return GROUPS_ID_LIST

  #
  # Using BS4 to parser group html source
  #
  # html_source = driver.page_source
  # soup = BeautifulSoup(html_source, 'lxml')
  # for groups in soup.find_all('a', {'class':'groupsRecommendedTitle'}):
  #   group_name = groups.string
  #   group_link = groups.get('href')


def facebook_post_to_groups(GroupId, GroupName, TextMessage, number_idx):
  url = FACEBOOK_URL + '/' + GroupId
  driver.get(url)
  clipboard.copy(TextMessage)
  sleep_time(4, count_down_msg = 'NO')

  try:
    TextAreaElem = driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
  except:
    print("%s %s on %s (%s) NoTextAreaElem" %(current_time(), TextMessage, GroupName, GroupId))
    return "NoTextAreaElem"

  # sleep_time(3, count_down_msg = 'NO')
  try:
    TextAreaElem.send_keys("")

    # if os == darwin
    # Mac OsX issue : can not paste using command+v key.
    # ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    
    # elif os == win:
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    sleep_time(1, "N")

    # driver.implicitly_wait(3) # seconds
  except:
    print("%s %s on %s (%s) send key failed" %(current_time(), TextMessage, GroupName, GroupId))
    return "SendKeyFailed"

  sleep_time(5, count_down_msg = 'NO')
  retry_count = 0
  while True:
    try:
      PostBtnElem = driver.find_element_by_xpath("//button/span[.='Post']").click()
      sleep_time(3, count_down_msg = 'NO')
      print('%s ============== Start post NO.%s ==============='   %(current_time(), number_idx))
      print("%s on %s (%s) successed" %(TextMessage, GroupName, GroupId))
      facebook_prsss_like_button()
      print('%s ============== End  post  NO.%s ===============\n' %(current_time(), number_idx))
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
  sleep_time(2, "N")
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

def facebook_prsss_like_button():
  print('%s Press like button' %current_time())
  like_btn_elem = driver.find_elements_by_xpath("//a[@data-testid='fb-ufi-likelink']")[0]
  like_btn_elem.click()

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

def get_account_info_from_file(account_file_path):
  if not (os.path.isfile(account_file_path) and os.access(account_file_path, os.R_OK)):
    print('%s is not exist' %account_file_path)
    exit();

  content_list = list()
  f = open(account_file_path, "r", encoding = 'utf-8')
  
  for line in f.readlines():                          
    if not len(line) or line.startswith('#'):     
      continue                                 
    line = line.strip(" \r\n")
    line = line.replace(" ","")
    content_list.append(line)
  return content_list

def get_article_number_list(fpath):
  filelist = []
  filelist = glob.glob(fpath)
  return filelist

def chrome_intialization():
  global driver
  notifications_block = 2
  ChromPrefs = GetChromeOptions_Notification(notifications_block)

  if sys.platform == 'win32':
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=ChromPrefs)

  if sys.platform == 'darwin':
    driver = webdriver.Chrome('./chromedriver', chrome_options=ChromPrefs)



# if sys.platform != 'win32' and sys.platform != 'darwin' :
#   display = Display(visible=0, size=(1600, 900))
#   display.start()


each_account_intervals_delay = 60 * 60
each_article_intervals_delay_min = 2 * 60
each_article_intervals_delay_max = 5 * 60

account_info_file_path_name = './account.cfg'
account_info_list = get_account_info_from_file(account_info_file_path_name)
account_info_list_len = len(account_info_list)
account_list_idx = 0
if (account_info_list_len == 0):
  print('Account file is not exist : please create "account" file')
  exit()

article_file_path = "./article/*"
article_path_list = get_article_number_list(article_file_path)
article_path_list_len = len(article_path_list)
if (article_path_list_len == 0):
  print('Article file is not exist : please create "./article/*"')
  exit()

post_count = 1
while True:
  process_start_time = datetime.now()
  next_start_time = process_start_time + timedelta(seconds = each_account_intervals_delay)

  account_info = account_info_list[account_list_idx].split(",")
  username = account_info[0]
  password = account_info[1]
  account_list_idx = account_list_idx + 1
  if (account_list_idx >= account_info_list_len):
    account_list_idx = 0


  chrome_intialization()
  cookies = dict()
  cookies = facebook_login(username,password)
  fb_groups_list = facebook_collect_groups_id()

  while process_start_time <= next_start_time:
    for fb_group_dict in fb_groups_list:
      for fb_group_id, fb_group_name in fb_group_dict.items():
        shuffle(article_path_list)
        rand_num = randint(0, article_path_list_len - 1)
        article_path = article_path_list[rand_num]
        msg = get_message_from_file(article_path)
        post_status = facebook_post_to_groups(fb_group_id, fb_group_name,  msg, post_count)

        # if post status failed, remove the gruoup from list.
        if (post_status == "SendKeyFailed") or (post_status == "NoTextAreaElem"):
          print("Remove %s %s" %(fb_group_id, fb_group_name))
          fb_groups_list.remove(fb_group_dict)
          break
          
        # if post successed then random sleep 2 ~ 4 mins
        rand_sleep_time(each_article_intervals_delay_min, each_article_intervals_delay_max)
        post_count += 1

        process_start_time = datetime.now()
        if process_start_time >= next_start_time:
          next_time = process_start_time + timedelta(seconds = each_account_intervals_delay)
          print("%s Sleeping....   next start time on %s" %(current_time(), next_time.strftime('%Y/%m/%d %H:%M:%S')))
          facebook_logout()
          driver.close()
          # sleep_time(each_account_intervals_delay)
          break

      if process_start_time >= next_start_time:
        break


# driver.close()
exit()


