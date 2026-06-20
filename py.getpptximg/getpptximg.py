from spire.presentation.common import *
from spire.presentation import *
import os

product = "KOSYAS-2026-06"

def getImg(fullname, filename):
    global product
    # Create a Presentation object
    presentation = Presentation()

    # Load a PowerPoint document
    #presentation.LoadFromFile("C:\\Users\\Administrator\\Desktop\\Input.pptx")
    presentation.LoadFromFile(fullname)

    # Get the images in the document
    images = presentation.Images
    
    if not os.path.exists(filename):
        os.makedirs(filename)

    title = filename.split(' ')
    # Iterate through the images in the document
    for i, image in enumerate(images):

        # Save a certain image in the specified path
#        ImageName = filename + "/Images_"+str(i)+".png"
        ImageName = filename + "\\" +product+ "_"+title[0]+"_"+f"{i+51:04d}"+".png"
        image_data = (IImageData)(image)
        image_data.Image.Save(ImageName)

    # Dispose resources
    presentation.Dispose()

def getSlide(fullname, filename):
    global product
    # Create a Presentation object
    presentation = Presentation()

    # Load a PowerPoint document
    #presentation.LoadFromFile("C:\\Users\\Administrator\\Desktop\\Input.pptx")
    presentation.LoadFromFile(fullname)

    # Get the images in the document
    images = presentation.Images
    
    if not os.path.exists(filename):
        os.makedirs(filename)

    title = filename.split(' ')
    # Iterate through the images in the document
    for i, slide in enumerate(presentation.Slides):

        # Save a certain image in the specified path
#        ImageName = filename + "/Images_"+str(i)+".png"
        ImageName = filename + "\\" +product+ "_"+title[0]+"_"+f"{i+51:04d}"+".png"
        image = slide.SaveAsImage()
        image.Save(ImageName)
        image.Dispose()

    # Dispose resources
    presentation.Dispose()

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
            getImg(fullname, filename)
#            getImg(fullname, filename)



search("C:\\0002.dev\\01.python\\getpptximg\\pptx")
