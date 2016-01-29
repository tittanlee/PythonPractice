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
import datetime
from bs4 import BeautifulSoup


FACEBOOK_URL = 'https://www.facebook.com'
GROUPS_ID_LIST = []

def sleep_time(seconds):
  print("sleep %s seconds" %seconds)
  time.sleep(seconds)

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


def facebook_collect_groups_id():
  print("collecting groups... wait a minutes")
  url = "https://www.facebook.com/groups/?category=membership"
  driver.get(url)

  GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")
  facebook_scroll_end_of_page() 
  GroupsElemsList = driver.find_elements_by_xpath("//*[@class='groupsRecommendedTitle']")

  print("total %s groups" %(len(GroupsElemsList)))
  for group in GroupsElemsList:
    group_name = group.text
    group_link = group.get_attribute('href') 
    group_id   = group.get_attribute('data-hovercard').split('=')[1]
    # print('%s %s %s' %(group_name, group_link, group_id))
    GROUPS_ID_LIST.append(group_id)

  #
  # Using BS4 to parser group html source
  #
  # html_source = driver.page_source
  # soup = BeautifulSoup(html_source, 'lxml')
  # for groups in soup.find_all('a', {'class':'groupsRecommendedTitle'}):
  #   group_name = groups.string
  #   group_link = groups.get('href')


def facebook_post_to_groups(GroupId, TextMessage):
  url = FACEBOOK_URL + '/' + GroupId
  driver.get(url)
  print("%s on %s prepared...." %(TextMessage, GroupId))
  try:
    TextAreaElem = driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
  except:
    print("%s on %s failed" %(TextMessage, GroupId))
    return "NoTextAreaElem"

  TextAreaElem .send_keys(TextMessage)
  # driver.implicitly_wait(3) # seconds
  sleep_time(3)
  while True:
    try:
      PostBtnElem = driver.find_element_by_xpath("//button/span[.='Post']").click()
      print("%s on %s successed" %(TextMessage, GroupId))
      break
    except:
      print("Post Button is not exist")
      sleep_time(3)


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
  url = 'https://developers.facebook.com/tools/explorer/145634995501895/'
  driver.get(url)

def facebook_scroll_end_of_page():
  lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  match=False
  while(match==False):
    lastCount = lenOfPage
    time.sleep(1)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
      match=True


# if sys.platform != 'win32' and sys.platform != 'darwin':
#   from pyvirtualdisplay import Display

init(autoreset=True)

parser = argparse.ArgumentParser(usage="-h for full usage")
parser.add_argument('-username', dest="username", help='facebook username to login with (e.g. example@example.com)',required=True)
parser.add_argument('-password', dest="password", help='facebook password to login with (e.g. \'password\')',required=True)

args = parser.parse_args()

username = args.username
password = args.password

# if sys.platform != 'win32' and sys.platform != 'darwin' :
#   display = Display(visible=0, size=(1600, 900))
#   display.start()

notifications_block = 2
ChromPrefs = GetChromeOptions_Notification(notifications_block)
driver = webdriver.Chrome('W:\\fb-group-crawler\\chromedriver.exe', chrome_options=ChromPrefs)


cookies = dict()
cookies = facebook_login(username,password)

# facebook_get_graphic_token()
facebook_collect_groups_id()
# print(GROUPS_ID_LIST)

for fb_group_id in GROUPS_ID_LIST:
  facebook_post_to_groups(fb_group_id, "http://beefun01.com/p/2423/")
  sleep_time(10)


# driver.close()
exit()


