import dlib
import tensorflow as tf
import numpy as np
import cv2
import os
from django.conf import settings

# path = 'C:/vscode/MulCam/etching/Makeup-Service/web/beautygan-django/beaurtyGAN/BG_model'

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('/var/www/models/shape_predictor_5_face_landmarks.dat')
sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.import_meta_graph('/var/www/models/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('/var/www/models'))
graph = tf.get_default_graph()

X = graph.get_tensor_by_name('X:0') # source
Y = graph.get_tensor_by_name('Y:0') # reference
Xs = graph.get_tensor_by_name('generator/xs:0') # output

def align_faces(img):
    dets = detector(img, 1)
    
    objs = dlib.full_object_detections()

    for detection in dets:
        s = sp(img, detection)
        objs.append(s)
        
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)
    
    return faces

def preprocess(img):
    return img.astype(np.float32) / 127.5 - 1.

def postprocess(img):
    return ((img + 1.) * 127.5).astype(np.uint8)
import os

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def makeupout(img, makeup):
    img1 = cv_imread(img)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img1_faces = align_faces(img1)
    src_img = img1_faces[0]
    img2 = cv_imread(makeup)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
    img2_faces = align_faces(img2)
    ref_img = img2_faces[0]

    X_img = preprocess(src_img)
    X_img = np.expand_dims(X_img, axis=0)
    Y_img = preprocess(ref_img)
    Y_img = np.expand_dims(Y_img, axis=0)

    output = sess.run(Xs, feed_dict={
        X: X_img,
        Y: Y_img
        })

    output_img = postprocess(output[0])
    result = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)
    src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
        
    return (src_img, result)
