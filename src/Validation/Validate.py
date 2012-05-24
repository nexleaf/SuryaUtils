#!/usr/bin/python



from scipy import diff
from scipy import nonzero

from Collections.SuryaUploadData import SuryaUploadData
from Collections.SuryaCalibrationData import *
from Collections.SuryaProcessResult import *


#class Validation:
    

def validate(result_item):
    if not isinstance(result_item, SuryaIANAResult):
        return False, ["Processing Not Successfull"]
    valid = True
    invalidmsgs = []
    ##
    # First check is to see if the gradient is valid
    #
    gradients = result_item.preProcessingResult.gradient
    if len(gradients) == 0:
        invalidmsgs.append("No gradient data, skipping validity check")
        valid = None
    else:
        redgrad = zip(*result_item.preProcessingResult.gradient)[0]
        diffgrad = diff(redgrad)
        if len(diffgrad[(diffgrad > 4)]) > 0:
            valid = False
            invalidmsgs.append("Gradient is not monitonically increasing!")
    return valid, invalidmsgs



