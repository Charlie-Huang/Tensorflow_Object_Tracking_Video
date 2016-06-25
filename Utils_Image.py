from PIL import Image, ImageChops,ImageDraw

size = (640,480)
img_save_type='PNG'
padding =[0,0]

def check_image_with_pil(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True

def resizeImage(file_path): 
    #Resize Cropping & Padding an image to the 640x480 pixel size

    image = Image.open(file_path)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    padding[0] = max( (size[0] - image_size[0]) / 2, 0 )
    padding[1] = max( (size[1] - image_size[1]) / 2, 0 )

    if((padding[0]==0) & (padding[1]==0)):
        image.save(file_path, img_save_type)
    else:
        thumb = image.crop( (0, 0, size[0], size[1]) )
        thumb = ImageChops.offset(thumb, int(padding[0]), int(padding[1]))
        thumb.save(file_path)

    return padding

def resize_saveImage(file_path, new_path): 
    #Resize Cropping & Padding an image to the 640x480 pixel size
    ##The method thumbnail mantain the aspect ratio and resize the image to fit the max size passed
    ##depending on the orientation of the image.
    ##Than with Image chops we set the smaller ones in 

    image = Image.open(file_path)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    padding[0] = max( (size[0] - image_size[0]) / 2, 0 )
    padding[1] = max( (size[1] - image_size[1]) / 2, 0 )

    if((padding[0]==0) & (padding[1]==0)):
        image.save(new_path, img_save_type)
    else:
        thumb = image.crop( (0, 0, size[0], size[1]) )
        thumb = ImageChops.offset(thumb, int(padding[0]), int(padding[1]))
        thumb.save(new_path)

    return padding

def getpadd_Image(file_path, size_0, size_1): 
    #Get Padd of the image

    image = Image.open(file_path)
    image.thumbnail((size_0,size_1)), Image.ANTIALIAS)
    image_size = image.size

    padding[0] = max( (size_0 - image_size[0]) / 2, 0 )
    padding[1] = max( (size_1 - image_size[1]) / 2, 0 )

    return padding







    




