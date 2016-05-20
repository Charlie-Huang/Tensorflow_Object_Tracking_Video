# Tensorflow_VID_Video_Object_Tracking

This Repository is my Master Thesis Project: "Develop a Video Object Detection with Tensorflow Technology" 
and it's still developing, so many updates will be made.
In this work, I used the architecture and problem solving strategy of the Paper T-CNN(Arxiv, http://arxiv.org/abs/1604.02532), that won last year IMAGENET 2015 (http://image-net.org/) Teaser Challenge VID (http://image-net.org/challenges/LSVRC/2015/results).
So the whole script architecture will be made of several component in cascade:
  - Still Image Detection (Return Tracking Results on single Frame);
    (This component could be unique or decompose into two sub-component:
      - First: determinate "Where" in the Frame;
      - Second: determinate "What" in the Frame.)
  - Temporal Information Detection( Introducing Temporal Information into the DET Results);
  - Context Information Detection( Introducing Context Information into the DET Results);
My project use many online tensorflow projects, as: 
  - YOLO Tensorflow (https://github.com/gliese581gg/YOLO_tensorflow);
  - TensorBox (https://github.com/Russell91/TensorBox).

[Now state of the Project]

  - Support only YOLO DET Algorithm;
  - Not support Training;
  - Not use of Temporal & Context Information;
  - Working on adapt TensorBox and GoogleNet in Cascade,to support Training and achive better accuracy;

[Script Usage]

To Run the script you have to had installed:
  - Tensorflow;
  - OpenCV;
  - Python;
All the Python library necessary could be installed easily trought pip install package_name.
To Test the script you have to open a Terminal window, go to the Repository directory and tape:

$ python tensorflow_video

You will see some Terminal Output like:

![alt tag](https://github.com/DrewNF/Tensorflow_VID_Video_Object_Tracking/blob/master/terminal_output_run.png)



