'''
Created on Nov 2, 2010

@author: surya
'''
'''
Created on Oct 30, 2010

@author: surya
'''

import os
import logging

from Logging.Logger import getLog

log = getLog('AppLock')
log.setLevel(logging.DEBUG)

def getLock(lockFileName, programName, level=logging.DEBUG):
    ''' Creates a lock file given by the lockname and puts a pid of the current process
        in the lock file. If the lock file exists it checks if the a process given by the
        pid in the lock file is running. If such a process exits it returns False indicating
        failure to create a lock file.  
        
        Returns:
        Boolean -- True if the process represented by programName isn't already running, False
                   otherwise.
        
    '''
    
    if os.path.exists(lockFileName):
        fh = open(lockFileName)
        pid = int(fh.readline())
        fh.close()
        psResult = os.system("ps -fp %i | grep -q %s" % (pid, programName))
        log.info("Running: ps -fp %i | grep -q %s" % (pid, programName))
        if psResult == 0:
            log.error("There can be only one instance of " + programName
                 + " Please check: " + lockFileName)
            return False
   
    # Create a new lock
    fh = open(lockFileName, 'w')
    fh.write("%i" % (os.getpid()))
    fh.flush()
    fh.close()
    os.chmod(lockFileName, 0777)
    log.info("Creating new lock file with pid({0:s}) to prevent dual running: {1:s} "
             .format(str(os.getpid()), lockFileName))
    return True