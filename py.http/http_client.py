import urllib, os
import urllib.request  ### python 3
#import urllib  ### python 2.7
import sys

HOST = "http://127.0.0.1:9090/files/"
DOWN_DIR = "http_downloads/"
FILELIST = 'ineedfilelist.a'

if not os.path.exists('http_downloads'):
    os.makedirs('http_downloads')

if not os.path.exists(FILELIST):
    print("I need a filelist!!!!!!!")
    sys.exit()

f = open(FILELIST,'r')
lines = f.readlines()
i = 0
for line in lines:
    try:
        targetName = line.strip()

        #urllib.urlretrieve (HOST + FILE_LIST_SERVER, FILE_LIST_CLIENT)
        urllib.request.urlretrieve  (HOST+ targetName, DOWN_DIR + targetName)
        print("Total %04d file(s) downloaded. [" % (i + 1) + targetName + "]")
        i = i+1
    except:
        print("error... & stop...")

f.close()

sys.exit()
