import random

def set_random_postion(max_height_grid_number, max_width_grid_number):
  random_height = random.randint(0, max_height_grid_number)
  random_width = random.randint(0, max_width_grid_number)
  return random_height, random_width

# NOTE: 画像を複数切り出す
# https://watlab-blog.com/2019/05/27/opencv-roi-copy/
# cropped_image = frosted_image[65:225, 15:200] # [left_y:right_y, left_x:right_x], right_y - right_x = grid にしたい
# image[65:225, 185:370] = cropped_image
def make_cropped_image(image, grid, random_height, random_width):
  cropped_image = image[
    grid*random_height:grid*random_height+grid,
    grid*random_width:grid*random_width+grid
  ]
  return cropped_image

def set_cropped_image_on_image(image, cropped_image, grid, random_height, random_width):
  image[
    grid*random_height:grid*random_height+grid,
    grid*random_width:grid*random_width+grid
  ] = cropped_image

def set_edited_image_on_image(
  edited_image,
  image,
  grid,
  before_edition_random_height_for_frosted_image,
  before_edition_random_width_for_frosted_image,
  after_edition_random_height_for_frosted_image,
  after_edition_random_width_for_frosted_image
):
  cropped_image = make_cropped_image(
    edited_image,
    grid,
    before_edition_random_height_for_frosted_image,
    before_edition_random_width_for_frosted_image
  )
  set_cropped_image_on_image(
    image,
    cropped_image,
    grid,
    after_edition_random_height_for_frosted_image,
    after_edition_random_width_for_frosted_image
  )