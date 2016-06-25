#### Import from Tensorbox


from utils.annolist import AnnotationLib as al

#### My import

from PIL import Image, ImageChops,ImageDraw
import progressbar
import time
import os
import sys

######### PARAMETERS

idl_filename='./dataset/antelope/antelope_bb_file_list.idl'

def test_IDL(idl_filename):
    
    progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])
    test_annos = al.parse(idl_filename)
    for test_anno in progress(test_annos):
        bb_img = Image.open(test_anno.imageName)
        for test_rect in test_anno.rects:
            dr = ImageDraw.Draw(bb_img)
            cor = (test_rect.x2,test_rect.y2,test_rect.x1,test_rect.y1 ) # DA VERIFICARE Try_2 (x1,y1, x2,y2) cor = (bb_rect.left() ,bb_rect.right(),bb_rect.bottom(),bb_rect.top()) Try_1
            dr.rectangle(cor, outline="green")
            bb_img.save(test_anno.imageName)


######### MAIN ###############

start = time.time()

test_IDL(idl_filename)

end = time.time()

print("Elapsed Time:%d Seconds"%(end-start))
print("Running Completed with Success!!!")
