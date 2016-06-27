# Import the necessary packages

import numpy as np
import cv2
import os
import time
import progressbar
import pandas
import sys

import Utils_Video

# Import DET Alg package
sys.path.insert(0, 'YOLO_DET_Alg')
import YOLO_small_tf

# DET Alg Params

# yolo.disp_console = (True or False, default = True)
# yolo.imshow = (True or False, default = True)
# yolo.tofile_img = (output image filename)
# yolo.tofile_txt = (output txt filename)
# yolo.filewrite_img = (True or False, default = False)
# yolo.filewrite_txt = (True of False, default = False)
# yolo.detect_from_file(filename)
# yolo.detect_from_cvmat(cvmat)

########## SETTING PARAMETERS

folder_path_det_frames='det_frames/'
folder_path_det_result='det_results/'
folder_path_summary_result='summary_result/'
file_name_summary_result='results.txt'
file_path_summary_result=folder_path_summary_result+'results.txt'
path_video='ILSVRC2015_val_00013002.mp4'
path_video_out='test.mp4'
video_perc=5


def still_image_YOLO_DET(frames_list, frames_name):
    print("Starting DET Phase")
    if not os.path.exists(folder_path_det_frames):
        os.makedirs(folder_path_det_frames)
        print("Created Folder: %s"%folder_path_det_frames)
    if not os.path.exists(folder_path_det_result):
        os.makedirs(folder_path_det_result)
        print("Created Folder: %s"%folder_path_det_result)
    yolo = YOLO_small_tf.YOLO_TF()
    det_frames_list=[]
    det_result_list=[]
    print("%d Frames to DET"%len(frames_list))
    progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])
    for i in progress(range(0,len(frames_list))):
        # det_frame_name = frames_name[i]
        det_frame_name = frames_name[i].replace('.jpg','_det.jpg')
        det_frame_name = folder_path_det_frames + det_frame_name
        det_frames_list.append(det_frame_name)
        
        det_result_name= frames_name[i].replace('.jpg','.txt')
        det_result_name = folder_path_det_result + det_result_name
        det_result_list.append(det_result_name)
        
        yolo.tofile_txt = det_result_name
        yolo.filewrite_txt = True
        yolo.disp_console = False
        yolo.filewrite_img = True
        yolo.tofile_img = det_frame_name
        yolo.detect_from_cvmat(frames_list[i][1])
    return det_frames_list,det_result_list


def print_YOLO_DET_result(det_results_list):
    results_list=[]
    if not os.path.exists(folder_path_summary_result):
        os.makedirs(folder_path_summary_result)
        print("Created Folder: %s"%folder_path_summary_result)
    print("Starting Loading Results ")
    progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])
    names=['class_name', 'x1','y1','x2','y2','score']
    df = pandas.DataFrame(columns=names)
    mean=0.0
    with open(file_path_summary_result, "w") as out_file:
        for i in progress(range(0,len(det_results_list))):
        #df.append(pandas.read_csv(det_results_list[i], sep=',',names=names, encoding="utf8"))
        #results_list.append(pandas.read_csv(det_results_list[i], sep=',',names=names, encoding="utf8"))
            for line in open(det_results_list[i], "r"):
                df.loc[i] =tuple(line.strip().split(','))
                mean=mean+float(df.loc[i].score)
                out_file.write(str(tuple(line.strip().split(',')))+ os.linesep)
    print("Finished Loading Results ")
    print("Computing Final Mean Reasults..")
    print "Class: " + df.class_name.max()
    print "Max Value: " + df.score.max()
    print "Min Value: " + df.score.min()
    print "Avg Value: " + str(mean/len(df))
    return

######### MAIN ###############

start = time.time()

frames, frame_list = Utils_Video.extract_frames(path_video, video_perc)
det_frame_list,det_result_list=still_image_YOLO_DET(frames, frame_list)
Utils_Video.make_video_from_list(path_video_out, det_frame_list)
end = time.time()
print_YOLO_DET_result(det_result_list)
print("Elapsed Time:%d Seconds"%(end-start))
print("Running Completed with Success!!!")
