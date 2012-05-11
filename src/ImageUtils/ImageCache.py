'''
Created on Nov 2, 2010

@author: surya
'''

'''
Created on Oct 30, 2010

@author: surya
'''

import os
import errno
import sys
import logging

from Logging.Logger import getLog


class ImageCache:
    ''' This class implements a simple disk based cache to store/remove images
    ''' 
    
    tags = "ImageCache"
    log = getLog('FileCache')
    
    def __init__(self, imageCachePath, level=logging.INFO):
        ''' Constructor
        
            Keyword Arguments:
            imageCachePath -- The path to the directory in which to store images
                               If the directory does not exist, its created.
            level          -- The logging level.
        '''
        
        # Set the logging level
        self.log.setLevel(level)
        
        try:
            os.makedirs(imageCachePath)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST:
                pass
            else: raise

        self.root = imageCachePath

    def put(self, filename, filedata):
        ''' Saves the filedata in a file represented by filename in the filecache
        
        Keyword Arguments:
        filename  -- The name of the file
        filedata  -- The data to store in the file
    
        Returns:
        String -- The Absolute file path if file was saved successfully, None otherwise
        '''
        absfilename = ""
        try:
            absfilename = self.root + "/" + filename
            fh = open(absfilename, "wb") #DEBUG
            fh.write(filedata)
            fh.close()
            os.chmod(absfilename, 0777)  #In Debug Mode, set the image file permission to 777
                
            self.log.info("Successfully saved the file '" + absfilename + "'", extra=self.tags) 
            return absfilename
        except:
            self.log.error("Failed to save the file '" + absfilename + "'" + ":" + str(sys.exc_info()[1]), extra=self.tags) 
            return None
        
    # TODO: maintain a list of files that we failed to delete and get a reaper to delete them later
    def remove(self, filename):
        ''' Removes the file represented by filename from the filecache
        
        Keyword Arguments:
        filename -- The name of the file
        '''
        
        os.remove(self.root+"/"+filename)
