import os, sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from time import localtime


##################################   Setting parameters ##################################
default_ip = '127.0.0.1'
default_port = 25
default_files = "C:\\03.work\\test\\smtp_test\\files"
loop_count = 5

ip = default_ip
port = default_port
files = default_files



#Set up crap for the attachments
#files = file_path
#filenames = [os.path.join(files, f) for f in os.listdir(files)]
#print filenames


#Set up users for email
gmail_user = "cylee@kisa.co.kr"
gmail_pwd = "somepasswd"
fromEmail = "cylee@kisa.co.kr"
toEmail = "cylee@kisa.co.kr"

#Create Module
def mail(to, subject, text, attach, filename):
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    #get all the attachments
    #   for file in filenames:
    part = MIMEBase('application', 'octet-stream')
    #      part.set_payload(open(file, 'rb').read())
    part.set_payload(open(attach, 'rb').read())
    encoders.encode_base64(part)
    #      part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
    #   part.add_header('Content-Disposition', 'attachment; filename="%s"' % attach)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
    msg.attach(part)

#   mailServer = smtplib.SMTP('localhost')
    if int(port) != 25:
      mailServer = smtplib.SMTP(ip)
    else:
      mailServer = smtplib.SMTP(ip, int(port))
#   mailServer.ehlo()
#   mailServer.starttls()
#   mailServer.ehlo()
#   mailServer.login(gmail_user, gmail_pwd)
#   mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.sendmail(fromEmail, toEmail, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.quit() #it's not here wins's apt dut has not get files.
    mailServer.close()

#send it


if len(sys.argv) != 4:
  print ("USAGE: <host> <port> <path>. if not I will use default parameters.")
else:
  _, in_ip, in_port, in_files = sys.argv
  try:
    port = int(port)
  except Exception:
    print ("Unknown port:", port)
  ip = in_ip
  port = in_port
  files = in_files


filenames = [os.path.join(files, f) for f in os.listdir(files)]

#for i in range(0, loop_count):
for i in range(0, len(filenames)):
  now = datetime.datetime.now()
  name = filenames[i].split('\\')
  n = len(name)
  print(str(now) + ' : ' +  filenames[i] + ' - '+ name[n-1])
  mail(toEmail, str(now) + " " + str('%06d' % i) , "Test email", filenames[i], name[n-1])
#  mail(toEmail, str(now) + " " + str('%06d' % i) , "Test email : " + name, filenames[i], str(os.getpid()) + '_' + name)
