import facebook
import fbconsole
import os
from urllib.parse import urlparse

TOKEN = 'CAACEdEose0cBAEJxayTM6S0szjQvbkcr5CU8GjESay51feLPlIoXykrhfQJ28nYGUrQC4q3XEaYZCds5ZCzmvlATFrMjo1tJOZA0Dss190ly9MaP4hYkgnXApZA3aSCVvd5JT2cMyhMt8ZC2fmsZCa1k6hJ8v1xhRpG1b2yt5Lp3K7HNTXJWSAhLjC3ZCb3Dwp0U0e5ledJWt9FjWEKcvt3'

BEEFUN01_GROUP_ID = '425409594316108'
Be001_Base_Url = 'http://beefun01.com/p/%s/?FB'


def write_data_to_file(filename, data):
  directory = './files'
  if not os.path.exists(directory):
    os.makedirs(directory)

  filepath = './files/' + filename + '.txt'
  f = open(filepath, 'w+', encoding = 'utf-8')
  f.write(data)
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
      write_data_to_file(file_name, msg + bee01_url_fb)
      idx = idx + 1
  except:
      print('#####  End  #####')
