#!/bin/bash


####
#### TODO:
## Track pid's of python processes ($! will be 'the process ID of the most recently executed background (asynchronous) command'
## Write signal handler to catch the Ctrl-C signal and kill those procs
#


source /home/surya/.virtualenvs/surya_bc/bin/activate

source /home/surya/deployed/set_surya_path.sh

cd $SURYA_DEPLOY_ROOT


# load any new calibrations
python -u $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/manage.py start $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/calibrationfile &> /dev/null

# Just touch files, hopefully mod_wsgi's daemon mode will reload everything
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/django.wsgi
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/settings.py


python -u $SURYA_DEPLOY_ROOT/SuryaIANAGmailPortal/src/GmailMonitor/IANAGmailMonitor.py -1 &> /dev/null &
GMM=$!

sleep 5

python -u $SURYA_DEPLOY_ROOT/SuryaIANAFramework/src/IANA/IANAFramework.py -1 &> /dev/null &
SIF=$!

sleep 15

python -u $SURYA_DEPLOY_ROOT/SuryaIANAGmailPortal/src/GmailResults/IANAGmailResults.py -1 &> /dev/null &
GMR=$!

sleep 5


# Let's see if closure type things work here
# function handle_sig() {
#     echo Killing PIDs $GMM $GMR $SIF
#     kill $GMM
#     kill $GMR
#     kill $SIF
#     echo "Killed..."
#     echo ""
#     exit 0
# }

# echo Setting trap for PIDs $GMM $GMR $SIF

# trap handle_sig SIGHUP SIGINT SIGTERM

#cd $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/

