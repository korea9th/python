import os, sys
import datetime
import codecs
import shutil
from time import localtime


##################################   Setting parameters ##################################
dirname = "2015"
default_files = "C:\\01.kisa\\01.files\\" + dirname + "년"
files = default_files

real_path = os.path.dirname(os.path.realpath(__file__))

#    f = open(dir + '\\' + filename, "r")
#Create Module
def parse(fullname, filename):
#    f = codecs.open(dirname + ".txt", "r", "utf-8")
    f = open(dirname + ".txt", "rb")
    lines = f.readlines()
    for line in lines:
#        print(filename + " : " + line)
        if filename.find(line.strip()) == 0:
            shutil.copy2(fullname, real_path + "\\" + dirname + "\\" + filename)
#            print(fullname + " : " + line)
    f.close()


#send it
def search(dirname):
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        if os.path.isdir(fullname):
            search(fullname)
        else:
#            print(fullname)
            parse(fullname, filename)
#            print(filename)



def read_ascii(filename):
	#    f = codecs.open(dirname + ".txt", "r", "utf-8")
    fout = open(filename + '.txt', 'wt')
#    fout = codecs.open(filename + '.txt', 'w', 'utf-8')
    f = open(filename, "rb")
    data = f.read()
    for i in range(0, sys.getsizeof(data) - sys.getsizeof('')):
        if (data[i] == 0x0a or data[i] == 0x0d) :
            fout.write('%c' % data[i])
#           print(' ')
        elif (data[i] > 31 and data[i] < 128) :
            fout.write('%c' % data[i])
#            print('%c'% data[i], end='', flush=True)
#        print(sys.getsizeof(data))
#        print(filename + " : " + line)
    f.close()
    fout.close()

#search(files)

read_ascii('ppee.exe')
#read_ascii('jpg.jpg')
#read_ascii('hwp.hwp')
#read_ascii('pdf.pdf')


'''
os.listdir(files)

filenames = [os.path.join(files, f) for f in os.listdir(files)]

#for i in range(0, loop_count):
#fout = codecs.open(dirname + '.txt', "w", "utf-8")
for i in range(0, len(filenames)):
    now = datetime.datetime.now()
    name = filenames[i].split('\\')
    n = len(name)
    print(name[n-2]+ '/'+ name[n-1])
#    parse(fout, str(now) + " " + str('%06d' % i) , "Test email", name[n-2], name[n-1])

#fout.close()
'''