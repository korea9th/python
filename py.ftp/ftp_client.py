from ftplib import FTP
import os
import sys

ftp = FTP()
host = "192.168.0.18"#"192.168.88.1"
port = 2121#8888

DOWN_DIR = 'download'
 
def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)
        
data = []

#ftp = FTP('192.168.30.34', '8888')     # connect to host, default port

ftp.connect(host,port)
ftp.login("admin", "123456")
#print( ftp.recv(1024))
#ftp.login()                     # user anonymous, passwd anonymous@
#ftp.cwd('debian')               # change into "debian" directory
#ftp.retrlines('PASV')           # list directory contents
#ftp.retrbinary('RETR README', open('README', 'wb').write)
print('get list........................')
lines = []
ftp.retrlines('LIST', lines.append)           # list directory contents
for i in range(0, len(lines)):
    print(lines[i])

print('\n\n')


#ftp.dir(data.append)

#upload(ftp, "README.txt")

if not os.path.exists(DOWN_DIR):
    os.makedirs(DOWN_DIR)

#ftp.retrbinary('RETR README.txt', open('README2.txt', 'wb').write)
print('get file........................')
for i in range(0, len(lines)):
    print((lines[i]))
    ftp.retrbinary('RETR ' + lines[i], open(DOWN_DIR + '/' + lines[i], 'wb').write)

ftp.quit()
 
#for line in data:
#    print ("-", line)
