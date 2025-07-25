import urllib, os
#import urllib.request  ### python 3
import urllib  ### python 2.7

HOST = "http://127.0.0.1:80/"
FILE_LIST = "smtpsend"

urllib.urlretrieve (HOST + FILE_LIST, FILE_LIST)

