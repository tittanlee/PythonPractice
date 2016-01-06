import requests
import base64
import sys, os
import codecs
import json
from bs4 import BeautifulSoup


Dict={}

Url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_t00.tw"
Res = requests.get(Url)
Res.encoding = 'utf-8'

soup = BeautifulSoup(Res.text, "html.parser")
Dict=json.loads(str(soup))

Msg = Dict['msgArray'][0]
print(Dict['queryTime']['sysTime'] ,Msg['t'], Msg['z'])
