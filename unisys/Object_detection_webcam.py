######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/20/18
# Description: 
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier and uses it to perform object detection on a webcam feed.
# It draws boxes, scores, and labels around the objects of interest in each frame
# from the webcam.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.


# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import math
from spellchecker import SpellChecker

spell = SpellChecker()

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from unisys.utils import label_map_util
from unisys.utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 26

## Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        #Intialize stuff for word correction
        self.k = 1
        self.j = 0
        self.i = 0
        self.c = []
        self.d = []
        self.sentence = []
        self.corrected_sentence = []
        self.word = ''
        self.final_sentence = ''

    def __del__(self):
        self.video.release()
    
    #function for mapping number to words
    def numToWord(self,x):
        if x == 1:
            return 'a'
        elif x == 2:
            return 'b'
        elif x == 3:
            return 'c'
        elif x == 4:
            return 'd'
        elif x == 5:
            return 'e'
        elif x == 6:
            return 'f'
        elif x == 7:
            return 'g'
        elif x == 8:
            return 'h'
        elif x == 9:
            return 'i'
        elif x == 10:
            return 'k'
        elif x == 11:
            return 'l'
        elif x == 12:
            return 'm'
        elif x == 13:
            return 'n'
        elif x == 14:
            return 'o'
        elif x == 15:
            return 'p'
        elif x == 16:
            return 'q'
        elif x == 17:
            return 'r'
        elif x == 18:
            return 's'
        elif x == 19:
            return 't'
        elif x == 20:
            return 'u'
        elif x == 21:
            return 'v'
        elif x == 22:
            return 'w'
        elif x == 23:
            return 'x'
        elif x == 24:
            return 'y'
        elif x == 25:
            return ''
        elif x == 26:
            return '.'
        else:
            return '_'

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):

        #variable to check if final sentence has been generated
        sentence_generated = False

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = self.video.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})


        scores_ = np.squeeze(scores)
        classes_ = np.squeeze(classes)

        if(max(scores_) >= 0.90):
            self.c.append(classes_[np.argmax(scores_)])
            self.i+=1
            if self.i==5:
                self.c = np.asarray(self.c, dtype = 'int64')
                self.d.append(np.bincount(self.c).argmax())
                self.i = 0
                print(self.d)
                self.c=[]

                if self.d[self.j] != self.d[self.j-1] and self.j!=0:
                    self.word+=self.numToWord(self.d[self.j-1])
                    print(self.word)

                if self.d[self.j]==25:
                    self.sentence.append(self.word)
                    self.word = ''

                if self.d[self.j]==26:
                    sentence_generated = True
                    self.sentence.append(self.word)
                    self.word = ''
                    
                    misspelled = spell.unknown(self.sentence)

                    for w in misspelled:
                        # Get the one `most likely` answer
                        self.corrected_sentence.append(spell.correction(w))
                    
                    self.final_sentence = ' '.join(self.corrected_sentence)
                    print(self.final_sentence)
                    
                    self.sentence = []
                    self.corrected_sentence=[]
                    self.final_sentence=''

                self.j+=1


        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4,
            min_score_thresh=0.90)
        
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), sentence_generated, self.final_sentence