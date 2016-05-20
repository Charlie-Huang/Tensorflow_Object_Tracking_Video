# Tensorflow_VID_Video_Object_Tracking

(Version 0.1, Last Update 20-05-2016)

## 1.Introduction

This Repository is my Master Thesis Project: "Develop a Video Object Detection with Tensorflow Technology" 
and it's still developing, so many updates will be made.
In this work, I used the architecture and problem solving strategy of the Paper T-CNN(Arxiv, http://arxiv.org/abs/1604.02532), that won last year IMAGENET 2015 (http://image-net.org/) Teaser Challenge VID (http://image-net.org/challenges/LSVRC/2015/results).
So the whole script architecture will be made of several component in cascade:
  1. Still Image Detection (Return Tracking Results on single Frame);
  2. Temporal Information Detection( Introducing Temporal Information into the DET Results);
  3. Context Information Detection( Introducing Context Information into the DET Results);

> Notice that the Still Image Detection component could be unique or decompose into two sub-component:
>  1. First: determinate "Where" in the Frame;
>  2. Second: determinate "What" in the Frame.


My project use many online tensorflow projects, as: 
  - YOLO Tensorflow (https://github.com/gliese581gg/YOLO_tensorflow);
  - TensorBox (https://github.com/Russell91/TensorBox).

## 2.Requirement & Installation
To install the script you only need to download the Repository.
To Run the script you have to had installed:
  - Tensorflow;
  - OpenCV;
  - Python;

All the Python library necessary could be installed easily trought pip install package_name.
To Test the script you have to open a Terminal window, go to the Repository directory and tape:

## 3.Script Usage
### Setting Parameters
  Into the script file, at the start, you will found this paragraph:
        
  ```python      
    folder_path_det_frames='det_frames/'
    folder_path_det_result='det_reults/'
    folder_path_summary_result='summary_result/'
    file_name_summary_result='results.txt'
    file_path_summary_result=folder_path_summary_result+'results.txt'
    path_video='input_video.mp4'
    path_video_out='output_video.mp4'
  ```
    
    
  Leave them as set, if you want to only try a run, otherwise you can change them to test on your own data.
  
  
### Usage
  After Set the Parameters, we can proceed and run the script:
  
  ```python
    python tensorflow_video
  ```
You will see some Terminal Output like:

![alt tag](https://github.com/DrewNF/Tensorflow_VID_Video_Object_Tracking/blob/master/terminal_output_run.png)

You will see a realtime frames output(like the one here below) and then finally all will be embedded into the Video Output( I uploaded the first two Test I've made in the folder /video_result, you can download them and take a look to the final result.
The first one has problems in the frames order, this is why you will see so much flickering in the video image,the problem was then solved and in the second doesn't show frames flickering ):

![alt tag](https://github.com/DrewNF/Tensorflow_VID_Video_Object_Tracking/blob/master/DET_frame_example.jpg)

## 4.Copyright

According to the LICENSE file of the original code,

  - Me and original author hold no liability for any damages
  - Do not use this on commercial!

## 5.State of the Project

  - Support only YOLO DET Algorithm;
  - Not support Training;
  - Not use of Temporal & Context Information;
  - Working on adapt TensorBox and GoogleNet in Cascade,to support Training and achive better accuracy;
