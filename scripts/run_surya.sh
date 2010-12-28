#!/bin/bash


####
#### TODO:
## Track pid's of python processes ($! will be 'the process ID of the most recently executed background (asynchronous) command'
## Write signal handler to catch the Ctrl-C signal and kill those procs
#




source set_surya_path.sh

cd $SURYA_DEPLOY_ROOT

/usr/bin/python2.6 -u $SURYA_DEPLOY_ROOT/SuryaIANAGmailPortal/src/GmailMonitor/IANAGmailMonitor.py &> /dev/null &
GMM=$!

/usr/bin/python2.6 -u $SURYA_DEPLOY_ROOT/SuryaIANAGmailPortal/src/GmailResults/IANAGmailResults.py &> /dev/null &
GMR=$!

/usr/bin/python2.6 -u $SURYA_DEPLOY_ROOT/SuryaIANAFramework/src/IANA/IANAFramework.py &> /dev/null &
SIF=$!

# Let's see if closure type things work here
function handle_sig() {
    echo Killing PIDs $GMM $GMR $SIF
    kill $GMM
    kill $GMR
    kill $SIF
    echo "Killed..."
    echo ""
    exit 0
}

echo Setting trap for PIDs $GMM $GMR $SIF

trap handle_sig SIGHUP SIGINT SIGTERM

#cd $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/

# To Run the Django Web Portal:
# NOTE: manage.py with start|stop|runserver
# Following order:
# python manage.py start
# python manage.py runserver
# manage.py stop <- this guy kills all daemons

/usr/bin/python2.6 -u $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/manage.py start $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/calibrationfile

# Removed since now using apache
#/usr/bin/python2.6 -u $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/manage.py runserver 8004
# Instead just touch files, hopefully mod_wsgi's daemon mode will reload everything
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/django.wsgi
touch $SURYA_DEPLOY_ROOT/SuryaWebPortal/src/SuryaWebPortal/settings.py

echo "Running in apache mode..."
while true; do
    # We infinite loop and sleep since we are not blocked on the django development webserver.
    # And we want to catch ctrl-c so we can properly kill off the three daemons started above.
    sleep 5
done



