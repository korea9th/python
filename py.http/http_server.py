#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import mimetypes as memetypes
import shutil
import os, sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from time import localtime


ip = '127.0.0.1'
port = 25
files = "C:\\000.bin\\01.python\\05.files"

fromEmail = "black@kisa.or.kr"
toEmail = "white@kisa.or.kr"

#Create Module
def mail(to, subject, text, attach, filename):
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
    msg.attach(part)
    if int(port) != 25:
        mailServer = smtplib.SMTP(ip)
    else:
        mailServer = smtplib.SMTP(ip, int(port))
    mailServer.sendmail(fromEmail, toEmail, msg.as_string())
    mailServer.quit() #it's not here wins's apt dut has not get files.
    mailServer.close()

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_headers(self):
        npath = os.path.normpath(self.path)
        print(os.getcwd()) ################################################################
        reqfile = files + npath #os.getcwd() + '/files' +  npath
        npath = npath[1:]
        path_elements = npath.split('/')
        print(npath) ################################################################
        print(path_elements) ################################################################

        print(reqfile) ################################################################

        if(npath == 'filelist.bin'):
            dir_files = files  #os.getcwd() + '/files'
            dir_list = os.getcwd() + '/list'
            if not os.path.exists(dir_list):
                os.makedirs(dir_list)
            filenames = [os.path.join(dir_files, f) for f in os.listdir(dir_files)]
            f = open(dir_list + '/filelist.bin', 'w')
            for i in range(0, len(filenames)):
                path, name = os.path.split(filenames[i])
                f.write(name)
                f.write('\n')
            f.close()
            self.send_response(200)
            self.end_headers()

            f = open(dir_list + '/filelist.bin', 'rb')
            shutil.copyfileobj(f, self.wfile)
            f.close()
            return

        if (npath == 'smtpsend'):
            filenames = [os.path.join(files, f) for f in os.listdir(files)]
            for i in range(0, len(filenames)):
                now = datetime.datetime.now()
                path, name = os.path.split(filenames[i])
                #  name = filenames[i].split('\\')
                #  n = len(name)
                print(str(now) + ' : ' +  filenames[i] + ' - '+ name)
                mail(toEmail, str(now) + " " + str('%06d' % i) , "Test email : " + name, filenames[i], str(os.getpid()) + '_' + name)
            self.send_response(200)
            self.end_headers()
            return





        if not os.path.isfile(reqfile) or not os.access(reqfile, os.R_OK):
            self.send_error(404, "file not found")
            print("404, file not found")
            return None

        content, encoding = memetypes.MimeTypes().guess_type(reqfile)
        if content is None:
            content = "application/octet-stream"

        info = os.stat(reqfile)

        self.send_response(200)
        self.send_header("Content-Type", content)
        self.send_header("Content-Encoding", encoding)
        self.send_header("Content-Length", info.st_size)
        self.end_headers()

        return reqfile

    def do_GET(self):
        elements = self.send_headers()
        if elements is None:
            print('return')  ################################################################
            return

        reqfile = elements
        f = open(reqfile, 'rb')
        shutil.copyfileobj(f, self.wfile)
        f.close()

        return
#        self._set_headers()
#        self.wfile.write("<html><body><h1>hi!</h1></body></html>")
  
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Title goes here.</title></head>")
        self.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        
        self.wfile.write("<body><p>%s</p>" % reqfile)
        self.wfile.write("</body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
