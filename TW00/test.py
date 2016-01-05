import requests
import base64
import sys, os
import codecs
from bs4 import BeautifulSoup


RowData = []
Data = [RowData]
Url = "http://www.taifex.com.tw/chinese/3/7_12_3.asp?COMMODITY_ID=TXF" 
Res = requests.get(Url)
Res.encoding = 'utf-8'

soup = BeautifulSoup(Res.text, "html.parser")
Table = soup.find('table', attrs={'class':'table_f'})
TableBody = Table.find('tbody')

# for Th in TableBody.find_all('th'):
  # Data.append(Th.string)
  # print(Th.string)
  # os.system("pause")


for Row in TableBody.find_all('tr'):
  for Th in Row.find_all('th'):
    RowData.append(Th.string) 

  # Data.append(RowData)
     # print(Th.string)

#   Cols = Row.find_all('td')
  # Cols = [ele.text.strip() for ele in Cols]
  # # Data.append([ele for ele in Cols if ele])
  # Data.append([ele for ele in Cols])
print(Data)

