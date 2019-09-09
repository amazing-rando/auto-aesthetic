from PIL import Image
from glob import glob
from random import choice, randint, uniform
from image_utils import *
import numpy as np
import os, cv2

#Set size of output image.
outsize = (1024,768)

#Make file lists.
imagedir = "./images/"
background = glob(imagedir + "background/*")
text = glob(imagedir + "text/*")
statue = glob(imagedir + "statue/*")
sticker = glob(imagedir + "sticker/*")
window = glob(imagedir + "window/*")

#Import random background image and resize to CANVAS SIZE.
im = Image.open(choice(background)).resize(outsize).convert("RGBA")

styles = ["cascade-box", "sticker", "statue"]
chosen = choice(styles)

if chosen == "cascade-box":
    #Make dialog box cascade.
    im = insert_cascade(choice(window), im, uniform(0.1, 0.3),
                        randint(0,256), randint(0,128))

    #Insert text
    x, y = [choice([50,550]), choice([50,450])]
    im = insert_pic(choice(text), im, 0, x, y)

elif chosen == "sticker":
    #Spam stickers at random locations and orientations.
    for _ in range(randint(10,20)):
        #Insert random sticker.
        x, y, k = [randint(-200, 900), randint(-200, 600), randint(0,364)]
        im = insert_pic(choice(sticker), im, k, x, y)

    #Insert text
    x, y = [choice([50,550]), choice([50,450])]
    im = insert_pic(choice(text), im, 0, x, y)

elif chosen == "statue":
    #Spam statues at random locations and orientations.
    for _ in range(randint(3,5)):
        #Insert random statue.
        x, y, k = [randint(-200, 900), randint(-200, 600), randint(0,364)]
        im = insert_pic(choice(statue), im, k, x, y)
        
    #Insert text
    x, y = [choice([50,550]), choice([50,450])]
    im = insert_pic(choice(text), im, 0, x, y)


#Save file.        
im.save("./aesthetic.png", "PNG")
