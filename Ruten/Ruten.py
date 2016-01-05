import requests
import base64
import sys, os
import codecs
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
}

cookies = {
    '_ts_id':  '999999999999999999', 
}

CSV_HEADER=("品名, 網址, 價錢, 剩餘數量, 已賣數量\n")
CSV_FILE_NAME="Ruten.csv"

def GetRutenItemRemainingNubmer(Url):
  ItemCount=[]
  ItemRequest = requests.get(Url, headers=headers, cookies=cookies)
  ItemRequest.encoding='utf-8'
  soup = BeautifulSoup(ItemRequest.text, "html.parser")
  for Idx in soup.findAll("strong", {'class' : 'text-medium number'}):
    ItemCount.append(Idx.string)
  return ItemCount


f = codecs.open(CSV_FILE_NAME,"w+")
f.write(CSV_HEADER)

SellerName=sys.argv[1]
RutenRequestUrl = "http://class.ruten.com.tw/user/index00.php?s=" + SellerName
ResRuten = requests.get(RutenRequestUrl, headers=headers, cookies=cookies)
ResRuten.encoding='utf-8'

soup = BeautifulSoup(ResRuten.text, "html.parser")
for DivItemInfo in soup.findAll("div", {'class' : 'item-info'}):
  ItemName = DivItemInfo.a.string
  ItemUrl  = DivItemInfo.a.get('href') 
  ItemPrice = DivItemInfo.find("span",{'class' : 'item-direct-price'}).string
  ItemPrice = (ItemPrice.splitlines()[2].strip(' \r\n\t')).replace(",","")
  ItemCountList = GetRutenItemRemainingNubmer(ItemUrl)
  ItemRemainCount = ItemCountList[0]
  ItemHasSellCount = ItemCountList [1]

  WriteLine = "%s, %s, %s, %s, %s\n" %(ItemName, ItemUrl, ItemPrice, ItemRemainCount, ItemHasSellCount)
  # print(WriteLine)
  f.write(WriteLine)

f.close()
