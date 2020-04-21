from PIL import Image


# In future do some math to have the default crop region be centred.
def crop(img):
    width, height = img.size
    aspect_ratio = height/width
    if(width>height):
        img = img.resize([int(400/aspect_ratio), 400])
    else:
        img = img.resize([600, int(600*aspect_ratio)])
    return img.crop((0, 0, 600, 400))

