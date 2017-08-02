#!/usr/bin/sh

#
# What it does:
# 1) cd to scripts base directory
# 2) Stops the running instance
# 3) Start Jenkins

working_dir=`dirname $0`
TOP=`pwd`

cd $working_dir
echo ""
echo "***********************************"
echo "Stopping Jenkins"
echo "***********************************"
echo ""

if [ ! -f stopJenkins.sh ]
then
   echo "stopJenkins.sh script does not exist under $working_dir"
  exit 1
fi
echo "Running $working_dir/stopJenkins.sh"

./stopJenkins.sh

if [ $? -ne 0 ]
then
  echo "Failed to stop Jenkins"
  exit 1
fi

echo ""
echo "***********************************"
echo "Starting Jenkins"
echo "***********************************"
echo ""
echo "Running $working_dir/startJenkins.sh"
echo ""
./startJenkins.sh

PID=`pgrep -fl jenkins.war | cut -d ' ' -f1`
cd $TOP

if [ "$PID" = "" ]
then
 echo "Failed to start Jenkins"
 echo ""
 echo "***********************************"
 echo ""
 exit 1
else
 echo "Jenkins started with new process ID: $PID"
 echo ""
 echo "***********************************"
 echo ""
 exit 0
fi
