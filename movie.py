import cv2

from lib.grid_line import grid_line
from lib.mosaic import mosaic
from lib.edges import edges
# from lib.face_detection import detect_face_and_eyes, is_face_detect
from lib.position import set_random_postion, make_cropped_image, set_cropped_image_on_image

input_video_path = './movies/inputs'
input_video_name = 'face'
capture = cv2.VideoCapture(input_video_path + '/' + input_video_name + '.mp4')

# NOTE: 元動画ファイルのFPS設定を取得する
fps = capture.get(cv2.CAP_PROP_FPS)

# NOTE: コーデック（エンコード・デコードするプログラムのこと，FourCCコードで識別される）を指定
# https://note.com/fz5050/n/n7fce725cbec6
fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # mp4フォーマットを指定

# NOTE: 動画の幅と高さを取得
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)

output_video_path = './movies/outputs'
output_video_name = "edited_{}".format(input_video_name)
edited_video = cv2.VideoWriter(
  "{}/{}.mp4".format(output_video_path, output_video_name),
  fourcc,
  fps,
  size,
)

i = 300

grid_numbers = 5

if width > height:
  grid = height // grid_numbers
  max_height_grid_number = grid_numbers - 1
  max_width_grid_number = int(max_height_grid_number * (width / height))
else:
  grid = width // grid_numbers
  max_width_grid_number = grid_numbers - 1
  max_height_grid_number = int(max_width_grid_number * (height / width))

random_postion_list = []
edition_types_nums = 4
a_type_edited_images_nums = 5
for i in range(edition_types_nums*a_type_edited_images_nums):
  before_random_height, before_random_width = set_random_postion(max_height_grid_number, max_width_grid_number)
  after_random_height, after_random_width = set_random_postion(max_height_grid_number, max_width_grid_number)
  random_postion_list.append([before_random_height, before_random_width, after_random_height, after_random_width])

print('START')
while True:
  # NOTE: 1フレームずつ取得
  # https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a57c0e81e83e60f36c83027dc2a188e80
  retval, image = capture.read()

  # NOTE: 動画が終了するとretvalが返らなくなる
  if not retval:
    break

  # TODO: --- 動画処理を追加する ----

  # NOTE: グレースケールに変換して誤認識を下げる
  # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # # NOTE: BGR変換: 動画ファイルとチャネル数（周波数）を合わせる
  # # https://tat-pytone.hatenablog.com/entry/2022/01/23/184808
  # changed_bgr_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

  # NOTE: エッジ検出
  edges_image = edges(image)

  # NOTE: すりガラス風モザイク
  frosted_image = cv2.blur(image, ksize=(20,20))

  # NOTE: 色反転
  reversal_color_image = cv2.bitwise_not(image)

  # NOTE: モザイク
  mosaic_image = mosaic(image, ratio=(1 / i))
  # i += 0.5

  type = 0
  for i in range(a_type_edited_images_nums):
    index = type * edition_types_nums
    # frosted_image
    cropped_image = make_cropped_image(frosted_image, grid, random_postion_list[index][0], random_postion_list[index][1])
    set_cropped_image_on_image(image, cropped_image, grid, random_postion_list[index][2], random_postion_list[index][3])

    index += 1
    # edges_image
    cropped_image = make_cropped_image(edges_image, grid, random_postion_list[index][0], random_postion_list[index][1])
    set_cropped_image_on_image(image, cropped_image, grid, random_postion_list[index][2], random_postion_list[index][3])

    index += 1
    # reversal_color_image
    cropped_image = make_cropped_image(reversal_color_image, grid, random_postion_list[index][0], random_postion_list[index][1])
    set_cropped_image_on_image(image, cropped_image, grid, random_postion_list[index][2], random_postion_list[index][3])

    index += 1
    # mosaic_image
    cropped_image = make_cropped_image(mosaic_image, grid, random_postion_list[index][0], random_postion_list[index][1])
    set_cropped_image_on_image(image, cropped_image, grid, random_postion_list[index][2], random_postion_list[index][3])

    type += 1

  # TODO: 顔検出して，目の複製はうまくいかず
  # if is_face_detect:
  #   face_img, trim_face_img, resize_right_eye_img, resize_left_eye_img = detect_face_and_eyes(image)

  #   print(trim_face_img, resize_right_eye_img, resize_left_eye_img)
  # else:
  #   face_img = image
  #   print("---")

  # # test
  # # NOTE: 画像重ねる, https://www.mathpython.com/opencv-image-add
  # if type(resize_right_eye_img) is list:
  #   right_eye_height, right_eye_width = resize_right_eye_img.shape[:2]
  #   # NOTE: 位置をズラす際は，同じ数値分足し算する必要がある．（例）: face_img[600:right_eye_height + 600, grid:right_eye_width + grid]
  #   face_img[grid*2:right_eye_height + grid*2, grid*2:right_eye_width + grid*2] = resize_right_eye_img

  # if type(resize_left_eye_img) is list:
  #   left_eye_height, left_eye_width = resize_left_eye_img.shape[:2]
  #   face_img[grid*1:right_eye_height + grid*1, grid*1:right_eye_width + grid*1] = resize_left_eye_img

  with_grid_line_img = grid_line(image, grid)

  # TODO: ------------------------

  # NOTE: VideoWriterに動画処理した1フレームを追加
  edited_video.write(image)

# NOTE: 動画ファイルを閉じる
# https://weblabo.oscasierra.net/python/opencv-videocapture-camera.html
edited_video.release()
capture.release()
# https://dev.classmethod.jp/articles/open-and-close-an-image-in-a-window-in-opencv/
cv2.destroyAllWindows()

print('END')


# 参考記事
# https://rikoubou.hatenablog.com/entry/2019/01/15/174751
# https://tat-pytone.hatenablog.com/entry/2022/01/23/184808
