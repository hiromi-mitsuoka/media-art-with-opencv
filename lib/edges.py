# https://qiita.com/shoku-pan/items/328edcde833307b164f4#sobel%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC

import cv2

def edges(img):
  img_sobel_x = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
  img_sobel_y = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)
  edges_img = cv2.hconcat([img_sobel_x, img_sobel_y])
  return edges_img