import cv2
import time

from lib.grid_line import grid_line
from lib.mosaic import mosaic
from lib.edges import edges
from lib.face_detection import detect_face_and_eyes

input_img_name = 'face02'

print("Start processing")
print("Please input img name")
output_img_name_suffix = input()

img_path = "./images/inputs/{}.jpg".format(input_img_name)
img = cv2.imread(img_path)

# TODO: --- 画像処理を追加する ----
# mosaic_img = mosaic(img, ratio=0.05)
# edges_img = edges(img, 50, 100)
face_img, trim_face_img, trim_right_eye_img, trim_left_eye_img = detect_face_and_eyes(img)

# NOTE: 画像重ねる, https://www.mathpython.com/opencv-image-add
right_eye_height, right_eye_width = trim_right_eye_img.shape[:2]
left_eye_height, left_eye_width = trim_left_eye_img.shape[:2]

# NOTE: 位置をズラす際は，同じ数値分足し算する必要がある．（例）: face_img[600:right_eye_height + 600, 300:right_eye_width + 300]
# face_img[0:right_eye_height, 0:right_eye_width] = trim_right_eye_img
face_img[300*5:right_eye_height + 300*5, 300*2:right_eye_width + 300*2] = trim_right_eye_img
face_img[300*6:right_eye_height + 300*6, 300*4:right_eye_width + 300*4] = trim_left_eye_img
face_img[300*1:right_eye_height + 300*1, 300*1:right_eye_width + 300*1] = trim_left_eye_img
time.sleep(2)
face_img[300*8:right_eye_height + 300*8, 300*7:right_eye_width + 300*7] = trim_right_eye_img
face_img[300*9:right_eye_height + 300*9, 300*3:right_eye_width + 300*3] = trim_right_eye_img
face_img[300*2:right_eye_height + 300*2, 300*6:right_eye_width + 300*6] = trim_left_eye_img

with_grid_line_img = grid_line(face_img)

# TODO: ------------------------

output_folder_path = './images/outputs'
cv2.imwrite("{}/{}_{}.jpg".format(output_folder_path, input_img_name, output_img_name_suffix), with_grid_line_img)

print("Finished processing")