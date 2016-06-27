




from xml.etree import ElementTree
import os
import shutil
import time
from PIL import Image, ImageChops
import progressbar
from Utils_Picture import Picture_Info, BB_Rectangle
import Utils_Image
import Utils
import Classes
from Classes import Classes_List as CL

##### STRING FILE NAMES #######

##MULTICLASS NEW DATASET

string_mltcl_bb_file = 'mltcl_bb_file_list.txt'
string_mltcl_class_code_file = 'mltcl_class_code_file_list.txt'
string_mltcl_class_name_file = 'mltcl_class_name_file_list.txt'
string_mltcl_chall_code_file = 'mltcl_chall_code_file_list.txt'

##SINGLE CLASS NEW DATASET

string_bb_file = '_bb_file_list.txt'
string_class_code_file = '_class_code_file_list.txt'
string_class_name_file = '_class_name_file_list.txt'
string_chall_code_file = '_chall_code_file_list.txt'

###DEFAULT PATHS

path_dataset='./dataset'

path_default_images_folder='image'

path_bb_folder = './ILSVRC2013_DET_bbox_val'

path_val_folder = './ILSVRC2013_val'

##### GENERAL FUNCTIONS

def create_summary_files(): #Create All the files needed for the New Dataset
    
    path_mltcl_bb_file= path_dataset+'/'+string_mltcl_bb_file
    path_mltcl_class_code_file= path_dataset+'/'+string_mltcl_class_code_file
    path_mltcl_class_name_file= path_dataset+'/'+string_mltcl_class_name_file
    path_mltcl_chall_code_file= path_dataset+'/'+string_mltcl_chall_code_file

    if not os.path.exists(path_dataset):
        os.makedirs(path_dataset)
        print("Created Folder: %s"%path_dataset)
    if not os.path.exists(path_mltcl_bb_file):
        open(path_mltcl_bb_file, 'a')
        print "Created File: "+ path_mltcl_bb_file
    if not os.path.exists(path_mltcl_class_code_file):
        open(path_mltcl_class_code_file, 'a')
        print "Created File: "+ path_mltcl_class_code_file
    if not os.path.exists(path_mltcl_class_name_file):
        open(path_mltcl_class_name_file, 'a')
        print "Created File: "+ path_mltcl_class_name_file
    if not os.path.exists(path_mltcl_chall_code_file):
        open(path_mltcl_chall_code_file, 'a')
        print "Created File: "+ path_mltcl_chall_code_file
    
    for class_name in CL.class_name_string_list:


        path_bb_file= path_dataset+'/'+class_name+'/'+class_name+string_bb_file
        path_class_code_file= path_dataset+'/'+class_name+'/'+class_name+string_class_code_file
        path_class_name_file= path_dataset+'/'+class_name+'/'+class_name+string_class_name_file
        path_chall_code_file= path_dataset+'/'+class_name+'/'+class_name+string_chall_code_file
        

        if not os.path.exists(path_dataset+'/'+class_name+'/'+path_default_images_folder):
            os.makedirs(path_dataset+'/'+class_name+'/'+path_default_images_folder)
            print("Created Folder: %s"%(path_dataset+'/'+class_name+'/'+path_default_images_folder))
        
        if not os.path.exists(path_bb_file):
            open(path_bb_file, 'a')
            print "Created File: "+ path_bb_file
        if not os.path.exists(path_class_code_file):
            open(path_class_code_file, 'a')
            print "Created File: "+ path_class_code_file
        if not os.path.exists(path_class_name_file):
            open(path_class_name_file, 'a')
            print "Created File: "+ path_class_name_file
        if not os.path.exists(path_chall_code_file):
            open(path_chall_code_file, 'a')
            print "Created File: "+ path_chall_code_file


##### MAIN ###############

### VARIABLES

bb_list=[]

width=640
heigh=480

####CALLs

start = time.time()
create_summary_files()
bb_list= Utils.get_Files_List(path_bb_folder)

count = 0

progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])

print "Start Processing & Building Dataset... may take a while..."

path_mltcl_bb_file=path_dataset+'/'+string_mltcl_bb_file # Create this file in .dataset/airplane/airplane_bb_mltcl_file_list.txt
path_mltcl_class_code_file=path_dataset+'/'+string_mltcl_class_code_file
path_mltcl_class_name_file=path_dataset+'/'+string_mltcl_class_name_file
path_mltcl_chall_code_file=path_dataset+'/'+string_mltcl_chall_code_file

for file_name in progress(bb_list):
    with open(file_name, 'rt') as f:
        tree = ElementTree.parse(f)
        for obj in tree.findall('object'):
            name = obj.find('name').text
            class_code= name
            name = Classes.code_to_class_string(name)

            if name in ["nothing"]:
                continue
            else:
                
                same_label=0
                
                count= count+1
                #The files with the original data path are made in both: multiclass e single class
                
                
                path_bb_file=path_dataset+'/'+name+'/'+ name+string_bb_file
                path_class_code_file= path_dataset+'/'+name+'/'+name+string_class_code_file
                path_class_name_file= path_dataset+'/'+name+'/'+name+string_class_name_file
                path_chall_code_file= path_dataset+'/'+name+'/'+name+string_chall_code_file


                path_new_file=path_dataset+'/'+name+'/'+path_default_images_folder
                path_orig_file=path_val_folder

                
                offset_x = 0
                offset_y = 0
                jump=0
                
                rectangles_single= Picture_Info()
                rectangles_single.dataset_path= path_dataset
                rectangles_single.folder=path_default_images_folder
                rectangles_single.default_path=path_val_folder

                rectangles_multi= Picture_Info()
                rectangles_multi.dataset_path= path_dataset
                rectangles_multi.folder=path_default_images_folder
                rectangles_multi.default_path=path_val_folder


                rectangle_single= BB_Rectangle()
                rectangle_multi= BB_Rectangle()
                
                #xmin x1 letf
                #ymin y1 bottom
                #xmax x2 right
                #ymax y2 top
            
                for node in tree.iter():
                    tag=str(node.tag)
        
                    # if tag in ["folder"]:
                        #path_orig_file=path_orig_file+'/'+str(node.text)

                    if tag in ["filename"]:
                        rectangles_single.filename=str(node.text)+'.PNG'
                        rectangles_multi.filename=str(node.text)+'.PNG'

                        path_orig_file=path_orig_file+'/'+str(node.text)+'.JPEG'
                        path_new_file=path_new_file+'/'+str(node.text)+'.PNG'

                    if tag in ['name']:
                        if str(Classes.code_to_class_string(str(node.text))) in ["nothing"]:
                            jump = 1
                        else : 
                            jump=0
                            rectangle_multi.label_chall=int(Classes.class_string_to_comp_code(str(Classes.code_to_class_string(str(node.text)))))
                            rectangle_multi.label_code=str(node.text)
                            rectangle_multi.label=Classes.code_to_class_string(str(node.text))

                            offset_x,offset_y=Utils_Image.resize_saveImage(path_orig_file, path_new_file)
                            #offset_x,offset_y=Utils_Image.getpadd_Image(path_orig_file, width, heigh)

                            if str(node.text) == class_code: 
                                same_label = 1
                                rectangle_single.label_chall=int(Classes.class_string_to_comp_code(str(Classes.code_to_class_string(str(node.text)))))
                            	rectangle_single.label_code=str(node.text)
                            	rectangle_single.label=Classes.code_to_class_string(str(node.text))
                            
                    if tag in ["xmax"]:
                        if jump == 0:
                            rectangle_multi.x2=float(float(node.text) + offset_x )
                            if same_label==1:
                            	rectangle_single.x2=float(float(node.text) + offset_x )
                    if tag in ["xmin"]:
                        if jump == 0:
                            rectangle_multi.x1=float(float(node.text) + offset_x )
                            if same_label==1:
                            	rectangle_single.x1=float(float(node.text) + offset_x )
                    if tag in ["ymax"]:
                        if jump == 0:
                            rectangle_multi.y2=float(float(node.text) + offset_y )
                            rectangles_multi.append_rect(rectangle_multi) 
                            if same_label==1:
                            	rectangle_single.y2=float(float(node.text) + offset_y )
                            	rectangles_single.append_rect(rectangle_single) 
                                same_label=0
                    if tag in ["ymin"]:
                        if jump == 0:    
                            rectangle_multi.y1=float(float(node.text) + offset_y )
                            if same_label==1:
                            	rectangle_single.y1=float(float(node.text) + offset_y )

                #shutil.copy2(path_orig_file, path_new_file)
                
                out_stream = open(path_bb_file, "a")
                out_stream.write(rectangles_single.get_info_string(True)+ os.linesep)
                
                out_stream = open(path_class_code_file, "a")
                out_stream.write(rectangles_single.get_rects_chall(True)+ os.linesep)
                
                out_stream = open(path_class_name_file, "a")
                out_stream.write(rectangles_single.get_rects_labels(True)+ os.linesep)
                
                out_stream = open(path_chall_code_file, "a")
                out_stream.write(rectangles_single.get_rects_code(True) + os.linesep)
                

                out_stream = open(path_mltcl_bb_file, "a")
                out_stream.write(rectangles_multi.get_info_string(False)+ os.linesep)
                
                out_stream = open(path_mltcl_class_code_file, "a")
                out_stream.write(rectangles_multi.get_rects_code(False)+ os.linesep)
                
                out_stream = open(path_mltcl_class_name_file, "a")
                out_stream.write(rectangles_multi.get_rects_labels(False)+ os.linesep)
                
                out_stream = open(path_mltcl_chall_code_file, "a")
                out_stream.write(rectangles_multi.get_rects_chall(False) + os.linesep)

                break


end = time.time()

print "bb_List_count:"+ str(len(bb_list))
print "count:"+ str(count)

print("Elapsed Time:%d Seconds"%(end-start))
print("Running Completed with Success!!!")

