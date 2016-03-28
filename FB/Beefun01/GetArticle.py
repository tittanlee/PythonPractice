import facebook
from fbconsole import *
import os
from urllib.parse import urlparse

TOKEN = 'CAACEdEose0cBAHYGZAlbq85fHaiSAWbvDgryzyirZCYRZBWHbVTLpy6LWLYUdObJhnLU6VKDYEvs9VplO6SEWZCg3Cvl8onrlaWpZBfIILhZCQY0ZBJNxLDJiZCphsXoz2wC4pnuA7vZCCjcm7Rx0OK9Q2sMTans75FrMjfj00Jir8DVhk2jTj7YHMAZA7GQR7HTW52XAU4AcNUQnzsoXoACYy'

BEEFUN01_GROUP_ID = '425409594316108'
Be001_Base_Url = 'http://beefun01.com/p/%s/?FB'
Bee01_Url_String = 'http://beefun01.com/p/'
                   

def write_data_to_file(filename, msg, link):
  directory = './article/'
  if not os.path.exists(directory):
    os.makedirs(directory)

  filepath = directory + filename + '.txt'
  f = open(filepath, 'w', encoding = 'utf-8')
  f.write(msg)
  f.write("\n")
  f.write(link)
  f.write("\n")
  f.write(" ")
  f.close()




graph = Client(TOKEN)

idx = 1
for d in iter_pages(graph.get('/' + BEEFUN01_GROUP_ID + '/feed', {'limit':25})):
  try:
    msg  = d['message']
    link = d['link']
  except KeyError:
    print('######   End Capture  ######')
    pass

  try:
    path_name = urlparse(link).path.split("/")
    if (path_name[2].isdigit()):
      file_name = path_name[2]
      bee01_url_fb = Be001_Base_Url %(file_name)
      print('\n######   NO.%s -- %s --  ######'  %(idx, file_name))

      if Bee01_Url_String in msg:
        b01_str_idx = msg.find(Bee01_Url_String)
        msg = msg[0:b01_str_idx]
      
      print(msg)
      print(bee01_url_fb)
      write_data_to_file(file_name, msg, bee01_url_fb)
      idx = idx + 1
  except:
      print('#####  End  #####')
