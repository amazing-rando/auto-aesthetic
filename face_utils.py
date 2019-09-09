from PIL import Image
import numpy as np
from random import choice, randint
from glob import glob
import cv2, math

def calcbounds(rect, off):
    '''
    Calculates upper left and lower right bounds for a given rect.
    '''
    ul = (rect[0] + off[0], rect[1] + off[1])
    lr = (rect[0] + rect[2] + off[2] , rect[1] + rect[3] + off[3])

    return ul, lr


def getrect(clf, gray, size, offset, k = 10):
    '''
    Returns the rectangular coordinates of detected feature.
    '''
    feature = clf.detectMultiScale(gray, 1.5, k)

    #Checks to see if the detected bounds make sense for a face.
    for f in feature:
        ul, lr = calcbounds(f, offset)
        #Upper bound should be positive & lower bound should be on right side.
        if ul[0] < 0 or lr[0] < size // 2:
            continue
        elif lr[1] - ul[1] > 300:
            continue
        else:
            break

    #If the best guess by the classifier is not believable, return None.
    if ul[0] < 0 or lr[1] < size // 2: #or lr[1] - ul[1] > 300:
        rect = None
    else:
        rect = [ul[0], ul[1], lr[0], lr[1]]

    return rect


def drag(im, rect):
    '''
    Corrupts a given image by pixel dragging within the specified rect.
    Returns corrupted image.
    '''
    #Get input image dimensions
    h, w, d = im.shape

    #Choose if drag should occur along horizontal or vertical dimensions.
    orientation = choice(["horizontal", "vertical"])
    if orientation == "vertical":

        #Choose a random direction along the vertical dimension and drag.
        offset = -90
        line = rect[1] + rect[3] // 2 + offset

        im[0:line, rect[0]:rect[0] + rect[2] + offset] = \
                im[line, rect[0]:rect[0] + rect[2] + offset]

    else:

        #Choose a random direction along the horizontal dimension and drag.
        line = randint(rect[0] + 50, rect[0] + rect[2] - 160)
        direction = choice(["left", "right"])

        if direction == "left":
            im[rect[1]:rect[1] + rect[3], 0:line] = \
                    im[rect[1]:rect[1] + rect[3], line:line + 1]
        else:
            im[rect[1]:rect[1] + rect[3], line:w] = \
                    im[rect[1]:rect[1] + rect[3], line:line + 1]

    return im


def stagger(im, rect):
    '''
    Corrupts a given image by pixel staggering to give a glitch effect around
    a given rect.  Returns the corrupted image.
    '''
    #Get input image dimensions.
    h, w, d = im.shape
    
    #Adjust offset.
    rect[0] -= 75

    #Define strip size.
    strip = rect[3] // randint(50, 90)
    n = rect[3] // (strip * 3)

    for i in range(n):

        #Define y axis limits.
        st_y = rect[1] + (i * strip)
        end_y = rect[1] + strip * (i + 1)

        #Define stagger constant.
        k = randint(1, 50)
        
        #Check to make sure image data is within image boundary.
        if rect[0] + rect[2] + k >= w:
            diff = rect[0] + rect[2] - w

            #Force stagger constant within bounds if its too big
            k = w - rect[0] + rect[2]

        #Glitch the image.
        diff = len(im[st_y:end_y, (rect[0] + k):rect[0] + rect[2] + k][1]) - \
                len(im[st_y:end_y, rect[0]:rect[0] + rect[2]][1])
        im[st_y:end_y, (rect[0] + k):rect[0] + rect[2] + k - diff] = \
            im[st_y:end_y, rect[0]:rect[0] + rect[2]]

    return im


def coverup(im, bar, rect):
    '''
    Places the provided censor bar image over the given rect.
    Returns censored image.
    '''
    #Convert numpy array to PIL Image for easy compositing.
    im = Image.fromarray(im).convert("RGBA")
    
    #Load censor bar image and preserve transparancy.
    imbar = Image.open(bar)
    
    #Resize censor bar.
    dim = (rect[2] - rect[0], rect[3] - rect[1])
    imbar = imbar.resize(dim)

    #Paste in censor bar and return numpy array.
    im.paste(imbar, (rect[0], rect[1]), imbar)
    im = np.array(im)
    
    return im


def modim(im, rect, offset, size, mod, bardir = None):
    '''
    Performs specified modification to a given image within rect.
    Returns modified image.
    '''
    if rect != None:
        
        #Get list of all censor bars.
        if bardir != None:
            bar = glob("./images/" + bardir + "/*")
            
            #Apply the specified modification.
            if mod == "cover" and bardir != None:
                im = coverup(im, choice(bar), rect)
            elif mod == "stagger":
                im = stagger(im, rect)
            elif mod == "drag":
                im = drag(im, rect)
                
    return im
