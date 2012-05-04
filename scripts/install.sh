#!/bin/bash

########################
## Install instructions
##

####
## Pull everything from git
##
#
#git clone git@github-MLL:nexleaf/SuryaUtils.git
#git clone git@github-MLL:nexleaf/SuryaIANAFramework.git
#git clone git@github-MLL:nexleaf/SuryaIANAGmailPortal.git
#git clone git@github-MLL:nexleaf/SuryaGmailPortal.git
#git clone git@github-MLL:nexleaf/SuryaDB.git
#git clone git@github-MLL:nexleaf/SuryaDANAFramework.git
#git clone git@github-MLL:nexleaf/SuryaWebPortal.git
#
#
#


####
## Setup install and run env
##
# Get this install.sh and the run_surya.sh file from SuryaUtils/scripts/ and put it in the directory
# where you cloned all the repos to.
#


####
## Make sure everything is installed
##
#
# sudo apt-get install python-matplotlib python-imaging python-kaa-base python-kaa-metadata python-numpy python-scientific
# sudo apt-get install python-opencv python-software-properties python-imaging-tk python-psyco
# 
# mongodb - http://www.mongodb.org/display/DOCS/Ubuntu+and+Debian+packages
# mongoengine - easy_install -U mongoengine
# easy_install -U pymongo
#




####
## Set working path
##

echo "Setting paths..."
export SURYA_DEPLOY_ROOT=/var/www/surya_bc
export SURYA_CODE_ROOT=`pwd`

export PYTHONPATH=$SURYA_DEPLOY_ROOT/SuryaDANAFramework/src:$SURYA_DEPLOY_ROOT/SuryaIANAFramework/src:$SURYA_DEPLOY_ROOT/SuryaIANAGmailPortal/src:$SURYA_DEPLOY_ROOT/SuryaGmailPortal/src:$SURYA_DEPLOY_ROOT/SuryaWebPortal/src:$SURYA_DEPLOY_ROOT/SuryaUtils/src:$SURYA_DEPLOY_ROOT/SuryaDB/src:$PYTHONPATH


####
## create path setup file
##

echo '#!/bin/bash' > set_surya_path.sh
echo " " >> set_surya_path.sh
echo "export SURYA_DEPLOY_ROOT=$SURYA_DEPLOY_ROOT" >> set_surya_path.sh
echo " " >> set_surya_path.sh
echo "export PYTHONPATH=$PYTHONPATH" >> set_surya_path.sh
echo " " >> set_surya_path.sh

chmod 775 set_surya_path.sh
source set_surya_path.sh

####
## copy files excluding the exclude files unless they do not exist
##

echo "Checking local settings are up to date... running diff:"
diff -uN SuryaIANAGmailPortal/src/IANAGmailSettings/Settings.py SuryaIANAGmailPortal/src/IANAGmailSettings/Settings_local.py
diff -uN SuryaWebPortal/src/SuryaWebPortal/settings.py SuryaWebPortal/src/SuryaWebPortal/settings_local.py

# add install
EXCLUDE_FILES_LIST="(install.sh)"

# fragile?
COPY_FILES=`find -type f | grep -v -E "(\.git|.*~|#)" | grep -v -E "$EXCLUDE_FILES_LIST"`

echo "Copying files..."
tar -cpf - $COPY_FILES | ( cd $SURYA_DEPLOY_ROOT; tar -xpf - )

echo "Final fixes..."
mkdir -p $SURYA_DEPLOY_ROOT/SuryaUtils/logs
chmod 777 $SURYA_DEPLOY_ROOT/SuryaUtils/logs
chmod 775 $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/manage.py

# for mod_wsgi daemon mode to rescan files
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/django.wsgi
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/settings.py

# for mod_wsgi to set all the paths correctly
echo "SuryaDANAFramework/src
SuryaIANAFramework/src
SuryaIANAGmailPortal/src
SuryaGmailPortal/src
SuryaWebPortal/src
SuryaUtils/src
SuryaDB/src" > $SURYA_DEPLOY_ROOT/surya.pth


# cd $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/
# ./manage.py syncdb

