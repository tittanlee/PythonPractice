#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

def sleep_time(seconds):
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
  url = "https://www.facebook.com/groups/?category=membership"
  driver.get(url)
  html_source = driver.page_source
  soup = BeautifulSoup(html_source, 'lxml')
  for groups in soup.find_all('a', {'class':'groupsRecommendedTitle'}):
    group_name = groups.string
    group_link = groups.get('href')


def facebook_post_to_groups():
  url = FACEBOOK_URL + '/groups/666064610178395/'
  driver.get(url)
  sleep_time(3)

  # div aria-autocomplete="list"
  elem = driver.find_element_by_xpath("//div[@class='groupComposerCleanWrap']")
  sleep_time(3)
  elem.send_keys(username)
  # print(elem)



if sys.platform != 'win32' and sys.platform != 'darwin':
  from pyvirtualdisplay import Display

init(autoreset=True)

parser = argparse.ArgumentParser(usage="-h for full usage")
parser.add_argument('-username', dest="username", help='facebook username to login with (e.g. example@example.com)',required=True)
parser.add_argument('-password', dest="password", help='facebook password to login with (e.g. \'password\')',required=True)

args = parser.parse_args()

username = args.username
password = args.password

if sys.platform != 'win32' and sys.platform != 'darwin' :
	display = Display(visible=0, size=(1600, 900))
	display.start()

# driver = webdriver.Firefox()
driver = webdriver.Chrome('W:\\fb-group-crawler\\chromedriver.exe')
action = webdriver.ActionChains(driver)

cookies = dict()
cookies = facebook_login(username,password)
# driver.switch_to.alert.dismiss()
sleep_time(1)

# facebook_collect_groups_id()
facebook_post_to_groups()


driver.quit()
exit()


