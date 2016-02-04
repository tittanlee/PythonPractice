import facebook
import fbconsole
import time

token = 'CAACEdEose0cBAMx2PGfIgzsuf2Y6Kfw3KUdqye5Xy6Qs3Xd9lucBmPxAxpP13K5wIrLTBQlb4WA1YiTkiCBq7c4z785hx9fyf3eRzUTDrCBsjqHuZBvLnuc3WfP6yJfxm8PkGuC784yP9954qZANR1jsWd4N5rVhr3xp19rU8rfC2dWtJ3NAaABj3ZCi1qxZCjsTknyAcwZDZD'


def writerfile(filename, data):
  path = './arctile/' + filename
  f = open(path, 'w', encoding = 'utf-8')
  f.write(data)
  f.close()





BEEFUN01_ID = '425409594316108'

graph = facebook.GraphAPI(token)
Beefun01_Content = graph.get_object(BEEFUN01_ID + "/feed")

idx = 1
for content in fbconsole.iter_pages(Beefun01_Content):
  try:
    msg  = content['message']
    link = content['link']
    

    print('##### No.%s #####' %idx)
    print('msg  = %s' %msg)
    print('link = %s' %link)
    
    try:
      start = link.index('p/')+2
      end   = link[start:].index('/') + start
      filename = link[start:end] + ".txt"
    except:
      break
      # filename = str(input('input filename:'))

    data = msg + "\n" + link
    writerfile(filename, data)

    idx += 1
  except KeyError:
    break

