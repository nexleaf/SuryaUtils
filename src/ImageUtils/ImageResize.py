

import os
import sys
import errno
import os.path
import logging
import StringIO
import PIL
import PIL.JpegImagePlugin
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from Logging.Logger import getLog



log = getLog("ImageResize")
log.setLevel(logging.ERROR)


def imageRotate(imagefile, deg):
    '''Rotate image'''
    # check for string or a mongo gridfs file object
    log.error("imagefile type is: " + str(imagefile.__class__))
    if isinstance(imagefile, str):
        if not os.path.isfile(imagefile):
            log.error('imagefile ' + imagefile + ' does not exist', extra=tags)
            return None, ExitCode.FileNotExists
        image = Image.open(imagefile)
    elif isinstance(imagefile, PIL.JpegImagePlugin.JpegImageFile) or isinstance(imagefile, PIL.Image.Image):
        image = imagefile
    else:
        # assume is already PIL type
        image = Image.open(StringIO.StringIO(imagefile.read()))
        #image = imagefile
    
    (x, y) = image.size
    log.error("In size: %d %d" % (x, y))

    newimage = image.rotate(deg, Image.BILINEAR, 1)

    (x, y) = newimage.size

    log.error("Out size: %d %d" % (x, y))

    return newimage
    


def imageResize(imagefile, largestside):
    '''Resize an image to what is specified as the long side'''
    # check for string or a mongo gridfs file object
    log.error("imagefile type is: " + str(imagefile.__class__))
    if isinstance(imagefile, str):
        if not os.path.isfile(imagefile):
            log.error('imagefile ' + imagefile + ' does not exist', extra=tags)
            return None, ExitCode.FileNotExists
        image = Image.open(imagefile)
    elif isinstance(imagefile, PIL.JpegImagePlugin.JpegImageFile) or isinstance(imagefile, PIL.Image.Image):
        image = imagefile
    else:
        # assume is already PIL type
        image = Image.open(StringIO.StringIO(imagefile.read()))
        #image = imagefile

    (x, y) = image.size

    log.error("In size: %d %d" % (x, y))
    
    # Find cleaner way to structure this
    # Is ANTIALIAS right? Maybe that messes with the color too much, os using BILINEAR
    if max(image.size) is not x:
        ratio = (y+0.0)/(x+0.0)
        smallside = largestside / ratio
        newimage = image.resize((int(smallside), int(largestside)), Image.BILINEAR)
    else:
        ratio = (x+0.0)/(y+0.0)
        smallside = largestside / ratio
        newimage = image.resize((int(largestside), int(smallside)), Image.BILINEAR)
    
    (x, y) = newimage.size

    log.error("Out size: %d %d" % (x, y))

    return newimage

