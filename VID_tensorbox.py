#### Import from Tensorbox

import tensorflow as tf
import matplotlib.pyplot as plt
import os
import json
import subprocess
from scipy.misc import imread

from train import build_forward
from utils import googlenet_load, train_utils
from utils.annolist import AnnotationLib as al
from utils.stitch_wrapper import stitch_rects
from utils.train_utils import add_rectangles
from utils.rect import Rect
from utils.stitch_wrapper import stitch_rects
from evaluate import add_rectangles
import cv2
import Utils_Image
import Utils_Video


#### My import

from PIL import Image, ImageChops,ImageDraw
import progressbar
import time
import os
import sys

########## SETTING PARAMETERS

folder_path_det_frames='det_frames/'
folder_path_frames='frames/'

folder_path_det_result='det_results/'
folder_path_summary_result='summary_result/'

file_name_summary_result='results.txt'
file_path_summary_result=folder_path_summary_result+'results.txt'

path_video='airplanes.mp4'
path_video_out='test.mp4'
path_video_folder = os.path.splitext(os.path.basename(path_video))[0]

video_perc=5


######### TENSORBOX PARAMETERS

hypes_file = './hypes/overfeat_rezoom.json'
weights_file= './output/save.ckpt-1090000'
pred_idl = './%s/%s_val.idl' % (path_video_folder, path_video_folder)
idl_filename=path_video_folder+'/'+path_video_folder+'.idl'

####### FUNCTIONS DEFINITIONS

def add_rectangles(H, orig_image, confidences, boxes, arch, use_stitching=False, rnn_len=1, min_conf=0.5, tau=0.25):
    from utils.rect import Rect
    from utils.stitch_wrapper import stitch_rects
    import numpy as np
    image = np.copy(orig_image[0])
    boxes_r = np.reshape(boxes, (-1,
                                 arch["grid_height"],
                                 arch["grid_width"],
                                 rnn_len,
                                 4))
    confidences_r = np.reshape(confidences, (-1,
                                             arch["grid_height"],
                                             arch["grid_width"],
                                             rnn_len,
                                             2))
    cell_pix_size = H['arch']['region_size']
    all_rects = [[[] for _ in range(arch["grid_width"])] for _ in range(arch["grid_height"])]
    for n in range(0, H['arch']['rnn_len']):
        for y in range(arch["grid_height"]):
            for x in range(arch["grid_width"]):
                bbox = boxes_r[0, y, x, n, :]
                conf = confidences_r[0, y, x, n, 1]
                abs_cx = int(bbox[0]) + cell_pix_size/2 + cell_pix_size * x
                abs_cy = int(bbox[1]) + cell_pix_size/2 + cell_pix_size * y
                h = max(1, bbox[3])
                w = max(1, bbox[2])
                #w = h * 0.4
                all_rects[y][x].append(Rect(abs_cx,abs_cy,w,h,conf))

    if use_stitching:
        acc_rects = stitch_rects(all_rects, tau)
    else:
        acc_rects = [r for row in all_rects for cell in row for r in cell if r.confidence > 0.0]


    for rect in acc_rects:
        if rect.confidence > 0.0:
            cv2.rectangle(image,
                      (rect.cx-int(rect.width/2), rect.cy-int(rect.height/2)),
                      (rect.cx+int(rect.width/2), rect.cy+int(rect.height/2)),
                      (0,255,0),
                      2)
    
    rects = []
    for rect in acc_rects:
        r = al.AnnoRect()
        r.x1 = rect.cx - rect.width/2.
        r.x2 = rect.cx + rect.width/2.
        r.y1 = rect.cy - rect.height/2.
        r.y2 = rect.cy + rect.height/2.
        r.score = rect.true_confidence
        rects.append(r)
    
    return image, rects





def still_image_TENSORBOX(idl_filename, frames_list):
    
    print("Starting DET Phase")
    
    if not os.path.exists(path_video_folder+'/'+folder_path_det_frames):
        os.makedirs(path_video_folder+'/'+folder_path_det_frames)
        print("Created Folder: %s"%path_video_folder+'/'+folder_path_det_frames)
    if not os.path.exists(path_video_folder+'/'+folder_path_det_result):
        os.makedirs(path_video_folder+'/'+folder_path_det_result)
        print("Created Folder: %s"% path_video_folder+'/'+folder_path_det_result)

    det_frames_list=[]

    #### START TENSORBOX CODE ###

    ### Opening Hypes file for parameters
    
    with open(hypes_file, 'r') as f:
        H = json.load(f)

    ### Get Annotation List of all the image to test
    
    test_annos = al.parse(idl_filename)

    ### Building Network

    tf.reset_default_graph()
    googlenet = googlenet_load.init(H)
    x_in = tf.placeholder(tf.float32, name='x_in', shape=[H['arch']['image_height'], H['arch']['image_width'], 3])

    if H['arch']['use_rezoom']:
        pred_boxes, pred_logits, pred_confidences, pred_confs_deltas, pred_boxes_deltas = build_forward(H, tf.expand_dims(x_in, 0), googlenet, 'test', reuse=None)
        grid_area = H['arch']['grid_height'] * H['arch']['grid_width']
        pred_confidences = tf.reshape(tf.nn.softmax(tf.reshape(pred_confs_deltas, [grid_area * H['arch']['rnn_len'], 2])), [grid_area, H['arch']['rnn_len'], 2])
    if H['arch']['reregress']:
        pred_boxes = pred_boxes + pred_boxes_deltas
    else:
        pred_boxes, pred_logits, pred_confidences = build_forward(H, tf.expand_dims(x_in, 0), googlenet, 'test', reuse=None)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        saver.restore(sess, weights_file )##### Restore a Session of the Model to get weights and everything working
    
        annolist = al.AnnoList()
        import time; t = time.time()
    
        #### Starting Evaluating the images
        lenght=int(len(frames_list))
        
        print("%d Frames to DET"%len(frames_list))
        
        progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])
        
        for i in progress(range(0, len(frames_list)-1)):
            img = imread(frames_list[i])
            feed = {x_in: img}
            (np_pred_boxes, np_pred_confidences) = sess.run([pred_boxes, pred_confidences], feed_dict=feed)

            pred_anno = al.Annotation()
            #pred_anno.imageName = test_anno.imageName
        
        
            new_img, rects = add_rectangles(H, [img], np_pred_confidences, np_pred_boxes,H["arch"], use_stitching=True, rnn_len=H['arch']['rnn_len'], min_conf=0.5)
            pred_anno.rects = rects
            bb_img = Image.open(frames_list[i])
            for bb_rect in rects:
            ################ Adding Rectangle ###################
                dr = ImageDraw.Draw(bb_img)
                cor = (bb_rect.x1,bb_rect.y1,bb_rect.x2 ,bb_rect.y2) # DA VERIFICARE Try_2 (x1,y1, x2,y2) cor = (bb_rect.left() ,bb_rect.right(),bb_rect.bottom(),bb_rect.top()) Try_1
                dr.rectangle(cor, outline="red")
                bb_img_det_name = frames_list[i].replace(folder_path_frames,folder_path_det_frames)
                bb_img.save(bb_img_det_name)
                det_frames_list.append(bb_img_det_name)
            annolist.append(pred_anno)

    annolist.save(pred_idl)

    #### END TENSORBOX CODE ###

    return det_frames_list


######### MAIN ###############

start = time.time()

idl_filename, frame_list = Utils_Video.extract_idl_from_frames(path_video, video_perc, path_video_folder, folder_path_frames, idl_filename )

progress = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ',progressbar.Percentage(), ' ',progressbar.ETA()])


for image_path in progress(frame_list):
    Utils_Image.resizeImage(image_path)

det_frame_list=still_image_TENSORBOX(idl_filename, frame_list)

Utils_Video.make_video_from_list(path_video_out, det_frame_list)

end = time.time()

print("Elapsed Time:%d Seconds"%(end-start))
print("Running Completed with Success!!!")
