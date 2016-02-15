import facebook
import fbconsole
import os
from urllib.parse import urlparse

TOKEN = 'CAACEdEose0cBANulj0uq8mwR5UZCi0nS9xMv5zZC49k0GhBTiZB7EImBrxYAvCSZAdl53px3bLhZCrGCqcIzH9ZBSswLbYuNHEo9oTLwLWZC0H5lFN5OVNZAVKcvYpCZC05A3g6hF77Py8R6qPvIEDKo8phVsBe89EjGqpNuGUEmcpougJQaSl0FRK9yrc8mhLB3sb0pglys56wZDZD'

BEEFUN01_GROUP_ID = '425409594316108'
Be001_Base_Url = 'http://beefun01.com/p/%s/?FB'


def write_data_to_file(filename, msg, link):
  directory = './article/'
  if not os.path.exists(directory):
    os.makedirs(directory)

  filepath = directory + filename + '.txt'
  f = open(filepath, 'w', encoding = 'utf-8')
  f.write(msg)
  f.write("\n")
  f.write(link)
  f.close()




graph = facebook.GraphAPI(TOKEN, version="2.3")
Beefun01 = graph.get_object(BEEFUN01_GROUP_ID + "/feed")
idx = 1
for d in fbconsole.iter_pages(Beefun01):
  try:
    msg  = d['message']
    link = d['link']
  except KeyError:
    print('######   End Capture  ######')
    break

  try:
    path_name = urlparse(link).path.split("/")
    if (path_name[2].isdigit()):
      file_name = path_name[2]
      bee01_url_fb = Be001_Base_Url %(file_name)
      print('######   NO.%s   ######'  %idx)
      print(msg)
      print(bee01_url_fb + '\n')
      write_data_to_file(file_name, msg, bee01_url_fb)
      idx = idx + 1
  except:
      print('#####  End  #####')
