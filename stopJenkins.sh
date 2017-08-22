#!/usr/bin/sh

###############################################
# Shell to stop the running instance of Jenkins
#
#####
PID=`pgrep -fl jenkins.war | cut -d ' ' -f1`

if [ "$PID" = "" ]
then 
  echo "Jenkins was not running"
  exit 0
fi
 
if [ $PID -ge 0 ]
then 
   echo "Stopping Jenkins  process ID : $PID"
   kill -9 $PID
fi

#
# Check that the process was killed
# if not exit with error
#
NPID=`pgrep -fl jenkins.war | cut -d ' ' -f1`

if [ "$NPID" = "" ]
then
  echo "Jenkins  process ID : $PID killed successfully "
  exit 0
else
 echo "Failed to kill Jenkins process $NPID"
 exit 1
fi
