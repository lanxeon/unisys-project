# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import math
from spellchecker import SpellChecker
import six.moves.urllib as urllib
import tarfile
import json


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


# added to put object in JSON
class Object(object):
    def __init__(self):
        self.name="webrtcHacks TensorFlow Object Detection REST API"

    def toJSON(self):
        return json.dumps(self.__dict__)

# Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def numToWord(x):
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
        print('(full-stop)')
        return '.'
    else:
        return '_'

#initialization variables
k = 1
j = 0
i = 0
c = []
d = []
sentence = []
corrected_sentence = []
word = ''
final_sentence = ''

#checking for a repeated letter
rep = 0

#variables to check if final sentence has been generated
sentence_generated = False
generated_sentence = None



def get_objects(image, autoCorrect):
    global k
    global j
    global i
    global c
    global d
    global rep
    global sentence
    global corrected_sentence
    global word
    global final_sentence

    global sentence_generated
    global generated_sentence

    #getting whether autocorrect value is true or not
    if autoCorrect=="true":
        auto = True
    else:
        auto = False

    #load the image into a numpy array
    frame = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    frame_expanded = np.expand_dims(frame, axis=0)


    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})


    scores_ = np.squeeze(scores)
    classes_ = np.squeeze(classes)

    if(max(scores_) >= 0.90):
        c.append(classes_[np.argmax(scores_)])
        i+=1
        if i==2:
            c = np.asarray(c, dtype = 'int64')
            if c[0]==c[1]:
                #d.append(np.bincount(c).argmax())
                d.append(c[1])
                i = 0
                print(d)
                c=[]

                if j==0:
                    word += numToWord(d[j])
                    print(word)

                if d[j] != d[j-1] and j!=0 and d[j]!=25 and d[j]!=26:
                    rep = 0
                    word += numToWord(d[j])
                    print(word)
                
                elif rep<=1 and d[j]!=25 and d[j]!=26:
                    rep+=1
                    word+= numToWord(d[j])
                    print(word)
                
                elif d[j]!=25 and d[j]!=26:
                    rep+=1

                if d[j]==25:
                    if word == '':
                        pass
                    sentence.append(word)
                    print(word)
                    word = ''

                if d[j]==26:
                    if word != '' or d[j-1]!=25:
                        print('word is:'+ word)
                        sentence_generated = True
                        sentence.append(word)
                        word = ''
                        
                        misspelled = spell.unknown(sentence)

                        for w in misspelled:
                            # Get the one `most likely` answer
                            corrected_sentence.append(spell.correction(w))
                        
                        if auto:
                            final_sentence = ' '.join(corrected_sentence)
                        else:
                            final_sentence = ' '.join(sentence)
                        
                        print(final_sentence)
                        generated_sentence = final_sentence
                        
                        sentence = []
                        corrected_sentence=[]
                        final_sentence=''

                j+=1
            
            else:
                i=0
                c=[]


    classes = np.squeeze(classes).astype(np.int32)
    scores = np.squeeze(scores)
    boxes = np.squeeze(boxes)


    output = []
    
    '''
    # Add some metadata to the output
    item = Object()
    item.version = "0.0.1"
    item.numObjects = obj_above_thresh
    item.threshold = threshold
    output.append(item)
    '''

    
    for lol in range(0, len(classes)):
        class_name = category_index[classes[lol]]['name']
        if scores[lol] >= 0.90:      # only return confidences equal or greater than the threshold
            #print(" object %s - score: %s, coordinates: %s" % (class_name, scores[c], boxes[c]))

            item = Object()
            item.name = 'Object'
            item.class_name = class_name
            item.score = float(scores[lol])
            item.y = float(boxes[lol][0])
            item.x = float(boxes[lol][1])
            item.height = float(boxes[lol][2])
            item.width = float(boxes[lol][3])
            item.sentence_generated = "false"
            item.generated_sentence = ""

            if sentence_generated:
                item.sentence_generated = "true"
                item.generated_sentence = generated_sentence 
                sentence_generated = False
                generated_sentence = None

            output.append(item)


    outputJson = json.dumps([ob.__dict__ for ob in output])
    return outputJson