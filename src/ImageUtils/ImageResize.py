

import os
import sys
import errno
import os.path
import logging
import StringIO
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from Logging.Logger import getLog



log = getLog("ImageResize")
log.setLevel(logging.ERROR)


def imageResize(imagefile, largestside):
    '''Resize an image to what is specified as the long side'''
    # check for string or a mongo gridfs file object
    if isinstance(imagefile, str):
        if not os.path.isfile(imagefile):
            log.error('imagefile ' + imagefile + ' does not exist', extra=tags)
            return None, ExitCode.FileNotExists
        image = Image.open(imagefile)
    else:
        # assume is already PIL type
        image = Image.open(StringIO.StringIO(imagefile.read()))
        #image = imagefile

    (x, y) = image.size

    # Find cleaner way to structure this
    # Is ANTIALIAS right? Maybe that messes with the color too much, os using BILINEAR
    if max(image.size) is not x:
        ratio = (y+0.0)/(x+0.0)
        smallside = largestside / ratio
        newimage = image.resize((smallside, largestside), Image.BILINEAR)
    else:
        ratio = (x+0.0)/(y+0.0)
        smallside = largestside / ratio
        newimage = image.resize((largestside, smallside), Image.BILINEAR)
    
    return newimage

