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
    def find_signals(self, frame):
        pass
