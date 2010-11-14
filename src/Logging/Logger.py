'''
Created on Nov 1, 2010

@author: surya
'''
import os
import logging
from logging.handlers import TimedRotatingFileHandler

ProjectName = 'SURYA'
LogFilename = os.path.dirname(__file__)+'/../../logs/SuryaLog'
Recurrance   = 'midnight'  # Seconds
TimeInterval = 1    # Time Interval after which to start logging new file


# Adding the 'projectname' specifiers
# They must be attributes of the log record

# Custom log record
class SuryaLogRecord(logging.LogRecord):
    def __init__(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        logging.LogRecord.__init__(self, name, level, fn, lno, msg, args, exc_info, func=None)
        self.projectname = ProjectName
        self.fileinfo = self.filename + ':' + str(lno)
        self.tags = extra
        
# Custom logger that uses our log record
class SuryaLogger(logging.getLoggerClass()):
            
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        return SuryaLogRecord(name, level, fn, lno, msg, args, exc_info, func=None, extra=extra)

def getLog(name):
    # Register Surya logger
    logging.setLoggerClass(SuryaLogger)
        
    logformat = "%(asctime)s %(projectname)s    %(fileinfo)+25s    %(levelname)-7s   : %(tags)s : %(message)s"
    # Set the logging format
    logging.basicConfig(level=logging.DEBUG, format=logformat)
    myLogger = logging.getLogger(name)
        
    # Add the log message handler to the logger
    timedFileHandler = TimedRotatingFileHandler(LogFilename, Recurrance, TimeInterval)
    timedFileHandler.setFormatter(logging.Formatter(logformat))
    
    myLogger.addHandler(timedFileHandler)
    
    return myLogger
