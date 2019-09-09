from PIL import Image
from random import randint, choice, Random

def insert_cascade(foreground_path, im, k = 0.01, x = 0,y = 0):
    '''
    Inserts a procedurally generated cascade of a given image.
    '''
    foreground = Image.open(foreground_path).convert("RGBA")
    background_size = im.size
    foreground_size = foreground.size
    acc = -1
    v = .0
    dy = .0
    
    #Calculate distance between image instances.
    for i in range(int(k * 100)): 
        dy = v * i + 0.5 * acc * (i ** 2)
        v = v + acc * i
        pos = (int(x +11* i), int(y - dy))
        im.paste(foreground, pos)

        if background_size[1] - foreground_size[1] <= pos[1]+foreground_size[1]:
            v = -v
            acc = acc * 0.9

    return im

def insert_pic(foreground_path, im, k=0, x=0, y=0):
    '''
    Inserts an image at the specified location with a given rotation and scale.
    '''
    foreground = Image.open(foreground_path).convert("RGBA")
    pos = (x, y)
    foreground = foreground.rotate(k*100)
    im.paste(foreground, pos, foreground)
    return im
