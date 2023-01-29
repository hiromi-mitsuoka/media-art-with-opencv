import cv2

def mosaic(img, ratio=0.1):
  h, w = img.shape[:2]
  # print(h, w, img.shape)

  reduced_img = cv2.resize(
    img,
    dsize=None,
    fx=ratio,
    fy=ratio,
    interpolation=cv2.INTER_NEAREST,
  )

  enlarged_img = cv2.resize(
    reduced_img,
    dsize=(w, h),
    interpolation=cv2.INTER_NEAREST,
  )

  return enlarged_img