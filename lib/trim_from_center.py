# https://pctraveljournal.com/?p=773

def trim_from_center(img, edited_width=300, edited_height=300):
  ch, cw = img.shape[:2]

  top = int((ch/2) - (edited_height/2))
  bottom = top + edited_height
  left = int((cw/2) - (edited_width/2))
  right = left + edited_width

  trim_from_center_img = img[top:bottom, left:right]

  return trim_from_center_img