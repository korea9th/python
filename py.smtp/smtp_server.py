import smtpd
import asyncore
import os
import email

i = 0
class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print ('Receiving message from:', peer)
        print ('Message addressed from:', mailfrom)
        print ('Message addressed to  :', rcpttos)
        print ('Message length        :', len(data))

        msg = email.message_from_string(data)
        attachments=msg.get_payload()
        for attachment in attachments:
            fnam=attachment.get_filename()
            if (fnam != None) :
                print (fnam)
                break;

#        f = open('emls/'+str('%06d' % i)+'.eml', "wb")
        f = open('emls/'+ str(fnam) +'.eml', "wb")
        f.write(data.encode())
        f.close()
#        i = i+1



        return

if not os.path.exists('emls'):
    os.makedirs('emls')

print ("starting SMTP server...")        
server = CustomSMTPServer(('127.0.0.1', 25), None)

try:
    asyncore.loop()
except KeyboardInterrupt:
    server.close()
