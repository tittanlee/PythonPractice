import facebook
import fbconsole
from urllib.parse import urlparse

TOKEN = 'CAACEdEose0cBAHq65mDOXGmiOSnbSVYJtZCVNos5ZCo9rrr33VYsH1BITUj59we64mSM1es6uQDtI2KvNtBi8vrcvRtmxTdzHVxm2Hq8SbQBZB7gZAq7wbBUFyPnfZBWR0JmHwgEN8bP4F0sikXYyZAyz7bqSGhzCWqOFKez39NqOel6ElajyMTpKLZAOWG9oXEF9X4exykJf6xGhQLvtE9'

BEEFUN01_GROUP_ID = '425409594316108'

Be001_Base_Url = 'http://beefun01.com/p/%s/?FB'

graph = facebook.GraphAPI(TOKEN, version="2.3")
Beefun01 = graph.get_object(BEEFUN01_GROUP_ID + "/feed")


def write_data_to_file(filename, data):
  filepath = './files/' + filename + '.txt'
  f = open(filepath, 'w', encoding = 'utf-8')
  f.write(data)
  f.close()

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
      idx += 1
  except:
      print('#####  End  #####')

  if (idx == 44):
    break


