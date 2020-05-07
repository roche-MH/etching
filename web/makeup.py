import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np
import cv2

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('models/shape_predictor_5_face_landmarks.dat')
sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.import_meta_graph('models/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('models'))
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

def makeupout(img,makeup):
    if img != None and makeup != None:
        img1 = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
        img1_faces = align_faces(img1)

        img2 = cv2.cvtColor(cv2.imread(makeup), cv2.COLOR_BGR2RGB)
        img2_faces = align_faces(img2)
        src_img = img1_faces[0]
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

        return output_img