################################################################## pop3 server   ########################################################################


"""pypopper: a file-based pop3 server

Useage:
    python pypopper.py <port> <path_to_message_file>
"""
import logging
import os
import socket
import sys
import traceback
import binascii
import datetime

from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

default_ip = '127.0.0.1'
default_port = 3110 #110
default_files = "C:\\02.dev\\03.go_project\\GoPop3d\\receivedFiles"

#test_files = "C:\\02.dev\\03.go_project\\GoPop3d\\receivedFiles"#"C:\\000.bin\\01.python\\05.files"
test_files = "C:\\02.dev\\01.python\\testfiles"

ip = default_ip
port = default_port
files = default_files

#file_path = "C:\\Users\\KISA\\Downloads\\_JES.2.9.0.bundle-bin\\received-emails"
#files = file_path
#filenames = [os.path.join(files, f) for f in os.listdir(files)]

##################################### get eml files   #######################################

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


######################################################################################################


logging.basicConfig(format="%(name)s %(levelname)s - %(message)s")
log = logging.getLogger("pypopper")
log.setLevel(logging.INFO)

class GetOutOfLoop(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)


class ChatterboxConnection(object):
    END = "\r\n"
    def __init__(self, conn):
        self.conn = conn
    def __getattr__(self, name):
        return getattr(self.conn, name)
    def sendall(self, data, END=END):
        if len(data) < 50:
            log.debug("send: %r", data)
        else:
            log.debug("send: %r...", data[:50])
        data += END
        self.conn.sendall(data.encode())
#        self.conn.sendall(binascii.a2b_uu(data))

    def recvall(self, END=END):
        data = []
        while True:
#            chunk = self.conn.recv(4096)
            chunk__ = self.conn.recv(4096)
            chunk = chunk__.decode()
#            chunk = chunk__
            if END in chunk:
                data.append(chunk[:chunk.index(END)])
                break
            data.append(chunk)
            if len(data) > 1:
                pair = data[-2] + data[-1]
                if END in pair:
                    data[-2] = pair[:pair.index(END)]
                    data.pop()
                    break
        log.debug("recv: %r", "".join(data))
        return "".join(data)


class Message(object):
#    def __init__(self, filename):
    def __init__(self, data):
        print("============================================================")
        print(data)
        print("============================================================")
        cmd, num, lines = data.split()
        msg = open(filenames[int(num)-1], "r")
        try:
            self.data = data = msg.read()
            self.size = len(data)
#            self.top, bot = data.split("\r\n\r\n", 1)
#            self.bot = bot.split("\r\n")
            self.top, bot = data.split("\n\n", 1)
            self.bot = bot.split("\n")
        finally:
            msg.close()


def handleUser(data, msg):
    return "+OK user accepted"

def handlePass(data, msg):
    return "+OK pass accepted"

def handleStat(data, msg):
    filesize = 0
    for i in range(0, len(filenames)):
        filesize = filesize + os.path.getsize(filenames[i])
#        print(filenames[i])
    print( "handleStat : " + "+OK %i %i" % (i+1, filesize))
    return "+OK %i %i" % (i+1, filesize)

def handleList(data, msg):
    i = 0
    size = 0
    names = []
    for j in range(0, len(filenames)):
        path, name = os.path.split(filenames[j])
        names.append(name)
        i = i+1
        size = size + len(name)
    
    print("handleList : " + "+OK %d messages (%i octets)\r\n%s\r\n." % (i, size, '\r\n'.join(names)))
    return "+OK %d messages (%i octets)\r\n%s\r\n." % (i, size, '\r\n'.join(names))
#    return "+OK 1 messages (%i octets)\r\n1 %i\r\n." % (msg.size, msg.size)
#return "+OK %i messages (%i octets)\r\n%s\r\n." % (len(msgs), sum([msg.size for msg in msgs]), '\r\n'.join(["%i %i" % (msg.index, msg.size,) for msg in msgs]))

def handleTop(data, msg):
    cmd, num, lines = data.split()
#    assert num == "1", "unknown message number: %s" % num
    msgs = Message(data)
    lines = int(lines)
    text = msgs.top + "\r\n\r\n" + "\r\n".join(msgs.bot[:lines])
    return "+OK top of message follows\r\n%s\r\n." % text

def handleRetr(data, msg):
    log.info("message sent")
    cmd, num = data.split()
    print(filenames[int(num)-1])
    file = open(filenames[int(num)-1], "r")
    try:
        body = file.read()
        size = len(body)
    finally:
        file.close()

    print("+OK %i octets\r\n%s\r\n." % (size, body))
#    print("+OK %i octets\r\n." % (size))
    return "+OK %i octets\r\n%s\r\n." % (size, body)
    
#    return "+OK %i octets\r\n%s\r\n." % (msg.size, msg.data)

def handleDele(data, msg):
    return "+OK message 1 deleted"

def handleNoop(data, msg):
    return "+OK"

def handleQuit(data, msg):
    return "+OK pypopper POP3 server signing off"

dispatch = dict(
    USER=handleUser,
    PASS=handlePass,
    STAT=handleStat,
    LIST=handleList,
    TOP=handleTop,
    RETR=handleRetr,
    DELE=handleDele,
    NOOP=handleNoop,
    QUIT=handleQuit,
)

def serve(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        if host:
            hostname = host
        else:
            hostname = "localhost"
        log.info("pypopper POP3 serving on %s:%s", hostname, port)
        while True:
            msg = None
            print('-------------------------------------------------------')
            try:
                sock.listen(1)
                conn, addr = sock.accept()
                log.debug('Connected by %s', addr)
                print('Connected by %s', addr)
#                msg = Message(filename)
                conn = ChatterboxConnection(conn)
                conn.sendall("+OK pypopper file-based pop3 server ready")
                while True:
                    data = conn.recvall()
                    print(data)
                    command = data.split(None, 1)[0]
#                    msg = Message(data)
                    try:
                        cmd = dispatch[command]
#                        msg = Message(data)
                    except KeyError:
                        conn.sendall("-ERR unknown command")
                    else:
                        conn.sendall(cmd(data, msg))
                        if cmd is handleQuit:
                            raise GetOutOfLoop(1)
            except KeyboardInterrupt:
                log.info("pypopper stopped(interrupt 111)")
            finally:
                conn.close()
                msg = None
    except GetOutOfLoop:
        log.info("pypopper stopped(GetOutOfLoop)")
        pass                
    except SystemExit:
        log.info("pypopper stopped(system exit)")
    except Exception as ex:
        log.critical("fatal error", exc_info=ex)
    finally:
#        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ("USAGE: <host> <port> <path>. if not I will use default parameters.")

    else:
        _, in_ip, in_port, in_file = sys.argv
        try:
            in_port = int(in_port)
        except Exception:
            print ("Unknown port:", in_port)
            sys.exit(1)
        else:
            ip = in_ip
            port = in_port
            files = in_file




    filenames = [os.path.join(test_files, f) for f in os.listdir(test_files)]

    if not os.path.exists('emls'):
        os.makedirs('emls')
        gen_mails = Gen_Emails()
        #for i in range(0, loop_count):
        for i in range(0, len(filenames)):
            now = datetime.datetime.now()
            name = filenames[i].split('\\')
            n = len(name)
            print(str(now) + ' : ' +  filenames[i] + ' - '+ name[n-1])
            gen_mails.EmailGen(toEmail, str(now) + " " + str('%06d' % i) , "Test email : " +  name[n-1], filenames[i], str(os.getpid()) + '_' + name[n-1])


    filenames = [os.path.join(files, f) for f in os.listdir(files)]
    serve(ip, port)

