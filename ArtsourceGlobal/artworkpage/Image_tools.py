from PIL import Image



def crop(img):
    width, height = img.size
    aspect_ratio = height/width
    if(width >= 600 and height >= 400):
        return img.crop((0, 0, 600, 400))  # (left, upper, right, lower)
    else:
        if(width>height):
            img = img.resize([int(400/aspect_ratio), 400])
        else:
            img = img.resize([600, int(600*aspect_ratio)])
        return img.crop((0, 0, 600, 400))

