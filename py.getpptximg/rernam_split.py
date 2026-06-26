import os


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
            title = filename.split('.')
            new_fullname = os.path.join(dirname, title[0]+"."+title[2])
            os.rename(fullname, new_fullname)
#            getImg(fullname, filename)



search("C:\\0002.dev\\01.python\\getpptximg\\pptx_extracted")
