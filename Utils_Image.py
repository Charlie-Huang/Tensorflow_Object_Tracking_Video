from PIL import Image, ImageChops,ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import cv2

size = (640,480)
img_save_type='PNG'

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

    padding_0 = max( (size[0] - image_size[0]) / 2, 0 )
    padding_1 = max( (size[1] - image_size[1]) / 2, 0 )

    orig_img = cv2.imread(file_path, 0)
    cv2.imshow('Original Image',orig_img)
    cv2.waitKey(2)

    if((padding_0==0) & (padding_1==0)):
        image.save(file_path, img_save_type)
    else:
        thumb = image.crop( (0, 0, size[0], size[1]) )
        thumb = ImageChops.offset(thumb, int(padding_0), int(padding_1))
        thumb.save(file_path)

    resized_img = cv2.imread(file_path, 0)
    cv2.imshow('Resized Image',resized_img)
    cv2.waitKey(2)

def resize_saveImage(file_path, new_path): 
    #Resize Cropping & Padding an image to the 640x480 pixel size
    ##The method thumbnail mantain the aspect ratio and resize the image to fit the max size passed
    ##depending on the orientation of the image.
    ##Than with Image chops we set the smaller ones in 
    
    image = Image.open(file_path)
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size

    padding_0 = max( (size[0] - image_size[0]) / 2, 0 )
    padding_1 = max( (size[1] - image_size[1]) / 2, 0 )

    orig_img = cv2.imread(file_path, 0)
    cv2.imshow('Original Image',orig_img)
    cv2.waitKey(2)

    if((padding_0==0) & (padding_1==0)):
        image.save(new_path, img_save_type)
    else:
        thumb = image.crop( (0, 0, size[0], size[1]) )
        thumb = ImageChops.offset(thumb, int(padding_0), int(padding_1))
        thumb.save(new_path)

    resized_img = cv2.imread(new_path, 0)
    cv2.imshow('Resized Image',resized_img)
    cv2.waitKey(2)

    if not check_image_with_pil(new_path):
        print 'ERROR: Rename & Save for: %s'%new_path
    if check_image_with_pil(file_path):
        os.remove(file_path)
        #print 'Delected old File: %s'%file_path

    return padding

def getpadd_Image(size_img_0, size_img_1, max_size_0, max_size_1): 
    #Get Padd of the image
    orig_ratio=float(size_img_0/size_img_1)
    new_ratio=-1
    max_ratio=float(max(float(size_img_0/max_size_0),float(size_img_1/max_size_1)))
    new_img_0=int(size_img_0/max_ratio)
    new_img_1=int(size_img_1/max_ratio)
    new_ratio=int(new_img_0/new_img_1)
    if new_ratio is not int(max_ratio):
    	print "Ratio Error"
    padding[0] = max( (max_size_0 - new_img_0) / 2, 0 )
    padding[1] = max( (max_size_1 - new_img_1) / 2, 0 )

    return padding

def transform_point(size_img_0, size_img_1, max_size_0, max_size_1, point, xory):
    orig_ratio=float(size_img_0/size_img_1)
    new_ratio=-1
    max_ratio=float(max(float(size_img_0/max_size_0),float(size_img_1/max_size_1),1))
    # print 'Size W Img: %d'% size_img_0
    # print 'Size H Img: %d'% size_img_1
    # print 'Size MW Img: %d'% max_size_0
    # print 'Size MH Img: %d'% max_size_1
    # print 'Starting Point Img: %d'% point
    # print 'Max Ratio New Img: %d'%max_ratio
    if(max_ratio==1):
	if xory:
	   # print "x point"
    	   padding = max( (max_size_0 - size_img_0) / 2, 0 )
    	else: 
	   # print "y point"
           padding = max( (max_size_1 - size_img_1) / 2, 0 )
	point = point + padding
    else:   
	new_img_0=int(size_img_0/max_ratio)
	new_img_1=int(size_img_1/max_ratio)
	new_ratio=int(new_img_0/new_img_1)
	old_ratio=int(size_img_0/size_img_1)
	if new_ratio is not old_ratio:
	    print "Ratio Error %d : %d"%(new_ratio,old_ratio)
	if xory:
	    # print "x point"
    	    padding = max( (max_size_0 - new_img_0) / 2, 0 )
    	else:
	    # print "y point"
            padding = max( (max_size_1 - new_img_1) / 2, 0 )
    point = int(point/max_ratio)+ padding
    # print 'Padding Point Img: %d'%padding 
    # print 'Ending Point Img: %d'%point
    return point


def get_Image_List(path, ext):
    files_list=[]
    for path, subdirs,files in os.walk(path):
        for filename in files:
            if not filename.endswith(ext): continue
            files_list.append(os.path.join(path, filename))
    return files_list

def change_extension(file_path, ext_1, ext_2):
    #Resize Cropping & Padding an image to the 640x480 pixel size
    if check_image_with_pil(file_path):
    	image = Image.open(file_path)
	#print'Starting Path: %s'% file_path
    	
	new_path=file_path.replace(ext_1,ext_2)
    	#print'New Path: %s'%  new_path
	image.save(new_path, img_save_type)
   	if check_image_with_pil(new_path):
		#print 'Rename & Save completed Correct for: %s'%new_path 
		os.remove(file_path)
	else : print 'ERROR: Rename & Save for: %s'%new_path
