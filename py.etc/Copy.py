import os, sys
import datetime
import codecs
import shutil
import hashlib
from time import localtime


##################################   Setting parameters ##################################
dirs = ["2015", "2016", "2017"]
dirname = "2017"
default_files = "C:\\01.kisa\\01.files\\tims" + dirname
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


def hash256(fullname, filename):
    ext = os.path.splitext(filename)
    n = len(ext)
#    if (ext[n-1].find('mal') != -1) :
    if (1 == 1) :
        hasher = hashlib.sha256()
        f = open(fullname, "rb")
        data = f.read()
        filesize = len(data)
#        print(filesize)
        if (filesize > 8) :
            hasher.update(data)
#           print(fullname + '\t' + hasher.hexdigest())
            print(hasher.hexdigest() + '\t' + fullname +
                  '\t%02x%02x%02x%02x%02x%02x%02x%02x\t' % (ord(data[0]),ord(data[1]),ord(data[2]),ord(data[3]),ord(data[4]),ord(data[5]),ord(data[6]),ord(data[7])) +
                  '\t%c%c%c\t' % (data[0],data[1],data[2] ))
#            print('https://www.virustotal.com/ko/file/' + hasher.hexdigest() + '/analysis/' + '\t' + fullname +
#                  '\t%02x%02x%02x%02x%02x%02x%02x%02x\t' % (ord(data[0]),ord(data[1]),ord(data[2]),ord(data[3]),ord(data[4]),ord(data[5]),ord(data[6]),ord(data[7])) +
#                  '\t%c%c\t' % (data[0],data[1] ))
#         print(hasher.hexdigest() + '\t' + fullname)
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
            hash256(fullname, filename)
#            print(filename)


def copy(fullname, filename):
    f = open(os.getcwd() + "\\tims_selected_sp01_all.txt",'r')
    lines = f.readlines()
    for line in lines:
        fname = line.rstrip()
        print(fname)
        shutil.copy2(os.getcwd() +"\\" + fname, os.getcwd() +  "\\sp01\\" + os.path.basename(fname))
#        print(os.path.basename(line))
    f.close()

copy("a", "a")

#for onedir in dirs:
#    search(onedir)

    

#search('2015')
#read_ascii('mal.exe')
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
