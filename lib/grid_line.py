# https://dx-navigation.com/image-gridline/

def grid_line(img, step=300):
  y_img, x_img = img.shape[:2]
  y_img = int(y_img)
  x_img = int(x_img)

  # NOTE: floatだとエラー
  img[step:y_img:step, :, :] = 150
  img[:, step:x_img:step, :] = 150

  return img