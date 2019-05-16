############### Object Detection API Libraries ################
import tensorflow as tf
import numpy as np
import time
from distutils.version import StrictVersion
from collections import defaultdict
from utils import label_map_util
from utils import visualization_utils as vis_util

############# CV Libraries ###################################
import cv2
import math

from object_detection.utils import ops as utils_ops
class ObjDetection(object):
    def __init__(self):
        self.config_model()
        self.__start_conf()
        self.__load_model()
        self.__start_sess()
    def ___config_model(self, name = 'inference_graph', ptl = 'labelmap.pbtxt'):
        self.graph = None
        self.TENSOR = None
        self.NUM_ITERACOES = 10
        self.BATCH = 1
        self.SOMA = 0
        self.MODEL_NAME = name
        self.PATH_TO_LABELS = ptl
    def __start_conf(self):
        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
    def __load_model(self):
        with tf.gfile.GFile(self.MODEL_NAME + '/frozen_inference_graph.pb', "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name="prefix")
            self.graph = graph
    def __start_sess(self):
        with tf.Session(graph = self.graph) as sess:
            self.sess = sess
    def predict(self, frame):
        image_np_expanded = np.expand_dims(frame, axis=0)
        output_dict = self.sess.run(y, feed_dict={x: image_np_expanded})
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        if 'detection_masks' in output_dict:
            output_dict['detection_masks'] = output_dict['detection_masks'][0]
        return output_dict
        
