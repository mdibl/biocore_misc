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

src_dir="/opt/software/"
dest_server="ec2-user@ec2-18-232-77-165.compute-1.amazonaws.com"
dest_dir="/opt/software"

#rsync_options="--links --ignore-errors"
rsync_options=" -avz --exclude=.snapshot"

rsync $rsync_options $src_dir $dest_server:$dest_dir 


