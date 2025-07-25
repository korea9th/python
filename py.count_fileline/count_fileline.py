import os, sys
import datetime
from time import localtime


##################################   Setting parameters ##################################

files = "C:\\04.KISA\\klounge"

file_count = 0
line_count = 0
error_count = 0

file_error_count = 0
file_error_list = []
dir_count = 1
dir_error_list = []

#send it
def search(dirname):
    global file_count, line_count, error_count
    filenames = os.listdir(dirname)
    for filename in filenames:
        fullname = os.path.join(dirname, filename)
        if os.path.isdir(fullname):
#            print("Dir : " + fullname)
            search(fullname)
        else:
            fname, ext = os.path.splitext(fullname)
            if (ext == '.ts') :
                try:
                    f = open(fullname, 'r', encoding='UTF8')
                    lines = f.readlines() #english
#                    print(fullname, len(lines))
                    f.close()
                    line_count += len(lines)
                    file_count+=1
                except Exception as err:
                    print("OS error: {0}".format(err) + "   :   " + fullname)
#                    print("Errorrrrrrrrr......  " + fullname)
                    error_count+=1


def read_filelines(filename):
    print(filename)
    if os.path.isdir(filename):
        read_filelines(filename)
    else :
        fname, ext = os.path.splitext(filenames[i])
        if (ext != 'ts') :
            return
        else:
            f = open(filename, 'r')
            lines = f.readlines()
            print(filename, len(lines))
        #    for line in lines:
        #        print(line)
            f.close()
            
            

search(files)
print("file : " + str(file_count))
print("lines: " + str(line_count))
print("error: " + str(error_count))

'''
filenames = [os.path.join(files, f) for f in os.listdir(files)]

#for i in range(0, loop_count):
for i in range(0, len(filenames)):
    now = datetime.datetime.now()
    path, name = os.path.split(filenames[i])
    read_filelines(filenames[i])
#  print(str(now) + ' : ' +  filenames[i] + ' - '+ name)
'''
