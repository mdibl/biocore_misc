#!/bin/sh

rsync_prog=`which rsync`
if [ ! -f $rsync_prog ]
then
   echo $rsync_prog
   echo "'rsync' not installed on `pwd`"
   exit 1
fi

#rsync_options="--links --ignore-errors"
# make sure the connection is passwordless between the host
# and the destination server - https://www.centos.org/docs/5/html/5.1/Deployment_Guide/s3-openssh-dsa-key.html
# A trailing slash on the source changes this behavior to avoid creating 
# an additional directory level at the destination. You can think of a trailing / 
# on a source as meaning "copy the contents of this directory" as opposed 
# to "copy the directory by name",
#
#rsync_options="--links --ignore-errors"
# Added --rsync-path='/usr/bin/sudo /usr/bin/rsync' 
# to ensure that rsync was being run with elevated privileges remotely. 
# This corrected the issue I was having:
# rsync: send_files failed to open "/data/projects/DustinUpdike/Jesse_GLH-1/rsem/.Rhistory": Permission denied (13)

rsync_options=' -avz  --exclude=.snapshot'

prog_usage(){
   echo ""
   echo "Usage: ./$SCRIPT_NAME  SOURCE DESTINATION"
   echo ""
}
#Check the number of arguments
if [ $# -lt 2 ]
then
  echo "***********************************************"
  prog_usage
  exit 1
fi
src_dir=$1
dest_dir=$2
if [[ -z "$src_dir" || ! -d $src_dir ]]
then
  echo "***********************************************"
  echo "ERROR - Invalid source: $src_dir "
  prog_usage()
  exit 1
fi

if [[ -z "$dest_dir" || ! -d $dest_dir ]]
then
  echo "***********************************************"
  echo "ERROR - Invalid source: $dest_dir "
  prog_usage()
  exit 1
fi

rsync $rsync_options $src_dir $dest_dir  2>&1

if [ $? -ne 0 ]
then
   echo "Cmd: rsync $rsync_options $src_dir $dest_dir - FAILED"
   exit 1
fi
exit 0
