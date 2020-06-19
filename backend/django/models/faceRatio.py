from imutils import face_utils
import dlib
import numpy as np
import cv2
import math
from django.conf import settings

path = '/var/www/models'
predictor = dlib.shape_predictor(path+"/shape_predictor_81_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(path+'/shape_predictor_5_face_landmarks.dat')
def align_faces(img):
    dets = detector(img, 1)
    if len(dets) == 0:
        return None
    objs = dlib.full_object_detections()
    
    for detection in dets:
        s = sp(img, detection)
        objs.append(s)
        
    faces = dlib.get_face_chips(img, objs, size=256, padding=0.5)
    
    return faces

# 거리구하기
def distance(p1,p2):
    x = p2[0] - p1[0]    # x좌표 길이
    y = p2[1] - p1[1]    # y좌표 길이
    distance = math.sqrt((x * x) + (y * y))
    return distance

def ratio2(a,b):
    ratio = [a/a, b/a]
    return ratio

def ratio3(a,b,c):
    ratio = [a/a, b/a, c/a]
    return ratio


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def faceLandmark81(frame):
    fr0 = cv_imread(frame)
    # gray = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_BGR2GRAY)
    fr1 = cv2.cvtColor(fr0, cv2.COLOR_BGR2RGB)
    fr = align_faces(fr1)
    if fr == None:
        return None
    fr = fr[0]
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for k, d in enumerate(rects):
        shape = predictor(gray, d)
        shape = face_utils.shape_to_np(shape)
        for (x, y) in shape:
            cv2.circle(fr, (x, y), 2, (0, 255, 0), -1)

    return cv2.cvtColor(fr, cv2.COLOR_RGB2BGR)


def faceRatio(frame):
    result={} 
    fr0 = cv_imread(frame)
    fr1 = cv2.cvtColor(fr0, cv2.COLOR_BGR2RGB)
    fr = align_faces(fr1)
    fr = fr[0]
    
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    for k, d in enumerate(rects):
            shape = predictor(gray, d)
            shape = face_utils.shape_to_np(shape)
            for (x, y) in shape:
                cv2.circle(fr, (x, y), 2, (0, 255, 0), -1)

    # [1] 눈:눈사이:눈
    left_eye = distance(shape[36], shape[39])
    between_eyes = distance(shape[42], shape[39])
    right_eye = distance(shape[45], shape[42])
    # 비율
    ratio_eyes = ratio3(left_eye, between_eyes, right_eye)
    eyes = "[1] 눈 : 눈 사이 : 눈 = {:.2f} : {:.2f} : {:.2f}\n".format(ratio_eyes[0], ratio_eyes[1], ratio_eyes[2])
    #result.append(eyes)
    if ratio_eyes[1]<1.3:
        result[eyes] = "눈 사이가 가까워요."
    elif ratio_eyes[1]>1.5:
        result[eyes] = "눈 사이가 멀어요."
    elif ratio_eyes[2]<0.9:
        result[eyes] = "사진상에서 왼쪽 눈이 더 커요."
    elif ratio_eyes[2]>1.1:
        result[eyes] = "사진상에서 오른쪽 눈이 더 커요."
    else:
        result[eyes] = "눈의 비율이 이상적입니다."

    # [2] 이마:중안부:하안부
    forehead = distance(shape[71], shape[27])
    midsection = distance((shape[21] + shape[22]) * 0.5, shape[33])
    lowersection = distance(shape[33], shape[8])
    # 비율
    ratio_section = ratio3(forehead, midsection, lowersection)
    section = "[2] 이마 : 중안부 : 하안부 = {:.2f} : {:.2f} : {:.2f}\n".format(ratio_section[0], ratio_section[1], ratio_section[2])
    #result.append(section)
    if ratio_section[1] > 1 and ratio_section[2] > 1:
        result[section] = "이마가 짧은편이에요."
    elif ratio_section[1] < 1 and ratio_section[2] < 1:
        result[section] = "이마가 긴편이에요."
    elif ratio_section[1] > 1.05:
        result[section] = "중안부가 긴편이에요."
    elif ratio_section[1] < 0.95:
        result[section] = "중안부가 짧은편이에요."
    elif ratio_section[2] > 1.05:
        result[section] = "하안부가 긴편이에요."
    elif ratio_section[2] < 0.95:
        result[section] = "하안부가 짧은편이에요."
    else:
        result[section] = "이마 : 중안부 : 하안부의 비율이 이상적입니다."

    # [3] 인중:턱
    philtrum = distance(shape[33], shape[62])
    jaw = distance(shape[62], shape[8])
    # 비율
    ratio_jaw = ratio2(philtrum, jaw)
    jaw = "[3] 인중 : 턱  = {:.2f} : {:.2f}\n".format(ratio_jaw[0], ratio_jaw[1])
    #result.append(jaw)
    if ratio_jaw[1] > 2.1:
        result[jaw] = "인중에 비해 턱이 긴 편입니다."
    elif ratio_jaw[1] < 1.9:
        result[jaw] = "인중에 비해 턱이 짧은 편입니다."
    else:
        result[jaw] = "인중과 턱의 비율이 이상적입니다."

    # [4] 얼굴 가로:얼굴 세로
    width = distance(shape[1], shape[15])
    length = distance((shape[69] + shape[72]) * 0.5, shape[8])
    # 비율
    ratio_width = ratio2(width, length)
    width = "[4] 얼굴 폭 : 얼굴 높이  = {:.2f} : {:.2f}\n".format(ratio_width[0], ratio_width[1])
    #result.append(width)
    if ratio_width[1] < 1.2:
        result[width] = "얼굴이 짧은 편입니다."
    elif ratio_width[1] > 1.4:
        result[width] = "얼굴이 긴 편입니다."
    else:
        result[width] = "얼굴 폭과 얼굴 높이의 비율이 이상적입니다."

    # [5] 코:입술
    nose = distance(shape[31], shape[35])
    mouth = distance(shape[48], shape[54])
    # 비율
    ratio_mouth = ratio2(nose, mouth)
    mouth = "[5] 코 : 입술  = {:.2f} : {:.2f}\n".format(ratio_mouth[0], ratio_mouth[1])
    #result.append(mouth)
    if ratio_mouth[1] > 2.05 :
        result[mouth] = "입술이 큰 편입니다."
    elif ratio_mouth[1] <1.95:
        result[mouth] = "입술이 작은 편입니다."
    else:
        result[mouth] = "입술의 비율이 이상적입니다."

    # [6] 코:얼굴 폭
    nose = distance(shape[31], shape[35])
    width = distance(shape[1], shape[15])
    # 비율
    ratio_nose = ratio2(nose, width)
    nose = "[6] 코 : 얼굴 폭  = {:.2f} : {:.2f}\n".format(ratio_nose[0], ratio_nose[1])
    #result.append(nose)
    if ratio_nose[1] > 5.8:
        result[nose] = "코가 작은편입니다."
    elif ratio_nose[1] < 5.0:
        result[nose] = "코가 큰편입니다."
    else:
        result[nose] = "코의 비율이 이상적입니다."


    # [7] 얼굴 가로:하관 가로
    width = distance(shape[0], shape[16])
    lower_width = distance(shape[4], shape[12])
    # 비율
    ratio_lower = ratio2(width, lower_width)
    lower = "[7] 얼굴 폭 : 하관 폭  = {:.2f} : {:.2f}\n".format(ratio_lower[0], ratio_lower[1])
    # result.append(lower)
    if ratio_lower[1] < 0.75:
        result[lower] = "하관이 좁은 편입니다.\n"
    elif ratio_lower[1] > 0.81:
        result[lower] = "하관이 넓은 편입니다."
    else:
        result[lower] = "하관의 비율이 이상적입니다."

    return result
