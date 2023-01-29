import cv2

from lib.trim_from_center import trim_from_center

def set_cascade():
    # 公式からダウンロードする必要あり．https://sh0122.hatenadiary.jp/entry/2017/10/30/210411
  face_cascade = cv2.CascadeClassifier('./lib/opencv-4.0.1/data/haarcascades/haarcascade_frontalcatface.xml')
  eye_cascade = cv2.CascadeClassifier('./lib/opencv-4.0.1/data/haarcascades/haarcascade_eye.xml')
  return face_cascade, eye_cascade

def detect_face(face_cascade, img):
  # NOTE: 第二引数はscaleFactor（デフォルト1.1），小さければ小さいほど顔の検出漏れが少なくなるものの、処理時間が長くなる
  # NOTE: 第三引数はminNeighbors（デフォルト3），小さければ小さいほど顔の検出漏れが少なくなりますが、誤検出が増える
  face = face_cascade.detectMultiScale(img, 1.1, 3)
  return face

def is_face_detect(img):
  face_cascade, _ = set_cascade()
  face = detect_face(face_cascade, img)

  if face != ():
    return True

  return False

def detect_face_and_eyes(img):
  face_cascade, eye_cascade = set_cascade()

  # if is_face_detect(img) == False:
  #   return img, 0, 0, 0

  face = detect_face(face_cascade, img)

  # NOTE: UnboundLocalErrorの防止
  face_img = img
  eyes = []

  # NOTE: 左上のx座標(x)、y座標(y)、顔の範囲の幅(w)、顔の範囲の高さ(h)
  for (x, y, w, h) in face:
    face_img = cv2.rectangle(img, (x,y), (x+w,y+h), (1,1,1), 1)
    roi_color = face_img[y:y+h, x:x+w]
    trim_face_img = img[
      y:y+h, # y軸の範囲: y~y+h
      x:x+w, # x軸の範囲: x~x+w
    ]
    eyes = eye_cascade.detectMultiScale(roi_color)

  eyes_list = []
  for (ex, ey, ew, eh) in eyes:
    cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (255,255,255), 1)
    trim_eye_img = trim_face_img[
      ey:ey+eh,
      ex:ex+ew,
    ]
    eyes_list.append(trim_eye_img)

  if len(eyes_list) < 2:
    return face_img, 0, 0, 0

  trim_right_eye_img = eyes_list[0]
  trim_left_eye_img = eyes_list[1]

  resize_right_eye_img = trim_from_center(trim_right_eye_img)
  resize_left_eye_img = trim_from_center(trim_left_eye_img)

  return face_img, trim_face_img, resize_right_eye_img, resize_left_eye_img