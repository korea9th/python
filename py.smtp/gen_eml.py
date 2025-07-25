from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime

fromEmail = "black@kisa.or.kr"
toEmail = "white@kisa.or.kr"
#    def __init__(self):
#        self.EmailGen()
class Gen_Emails(object):


    def EmailGen(self, to, subject, text, attach, filename):
        msg = MIMEMultipart()

#        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = fromEmail
        msg['To'] = toEmail

        msg.attach(MIMEText(subject))

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

        self.SaveToFile(msg, filename)


    def SaveToFile(self,msg, text):
    	text = text.replace(" ", "_") #'helloapple'
    	text = text.replace(":", "_") #'helloapple'
    	text = os.path.join(os.getcwd(), 'emls/' + text+'.eml')
        with open(text, 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(msg)

'''
        html = """\
        <html>
            <head></head>
            <body>
                <p> hello world </p>
            </body>
        </html>
        """
        part = MIMEText(html, 'html')

        msg.attach(part)
'''

files = "C:\\000.bin\\01.python\\05.files"

filenames = [os.path.join(files, f) for f in os.listdir(files)]

gen_mails = Gen_Emails()

if not os.path.exists('emls'):
    os.makedirs('emls')

#for i in range(0, loop_count):
for i in range(0, len(filenames)):
    now = datetime.datetime.now()
    name = filenames[i].split('\\')
    n = len(name)
    print(str(now) + ' : ' +  filenames[i] + ' - '+ name[n-1])
    gen_mails.EmailGen(toEmail, str(now) + " " + str('%06d' % i) , "Test email : " +  name[n-1], filenames[i], str(os.getpid()) + '_' + name[n-1])


