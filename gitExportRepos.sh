#!/bin/sh

#This script exports tags from public git repositories
#
# Assumption: None
#
# Input:
#   1) Owner/Organization name
#   2) Repository name
#   3) Tag
#
# What it does:
#    1) Set path to git tag
#    2) wget repos tag 
#    3) Create local directory for the new tag
#    4) Untar new tag tar 
#    5) Remove the downloaded tar file
#
# Author: lnh
# Date : 8/1/2017
#

WGET=`which wget`
TAR=`which tar`

#setup the log file
SCRIPT_NAME=`basename $0`
WORKING_DIR=`dirname $0`
LOG_DIR=$WORKING_DIR/logs

if [ ! -d $LOG_DIR ]
then
   mkdir $LOG_DIR
fi

LOG=$LOG_DIR/$SCRIPT_NAME.log
rm -f $LOG
touch $LOG

#Check the number of arguments
if [ $# -lt 3 ]
then
  echo ""
  echo "***********************************************"
  echo "Bad usage ---"
  echo "Usage: ./$SCRIPT_NAME ORGANIZATION/OWNER REPO_NAME GIT_TAG"
  echo "Example1: ./$SCRIPT_NAME mdibl data_downloads  1-0-4-3"
  echo "Example1: ./$SCRIPT_NAME mdibl biocore_misc  master"
  echo ""
  echo "***********************************************"
  echo ""
  exit 1
fi
##
ORG=$1
REPO=$2
TAG=$3

#Url to private repository
GIT_URL=https://api.github.com/repos/$ORG/$REPO/tarball/$TAG
#Local tag directory
TAG_DIR=$REPO-$TAG
#Results tar file
TAG_TAR_FILE=$TAG_DIR.tar.gz

date | tee -a $LOG
echo "wget path: $WGET" | tee -a $LOG
echo "tar path: $TAR"| tee -a $LOG
echo "Tag: $TAG"| tee -a $LOG
echo "Repository: $REPO"| tee -a $LOG
echo "Organization: $ORG"| tee -a $LOG
echo "Git url: $GIT_URL"| tee -a $LOG
echo "My Github personal token: $GTOKEN" | tee -a $LOG
date | tee -a $LOG

#execute the command
echo Cammand: $WGET -O $TAG_TAR_FILE  "$GIT_URL" | tee -a $LOG
$WGET -O $TAG_TAR_FILE  "$GIT_URL" | tee -a $LOG

#clean previous download of this tag
if [ -d $TAG_DIR ]
then
  rm -rf $TAG_DIR
fi
#Create local directory for this tag
mkdir $TAG_DIR

#Untar the new archive
echo "Untar $TAG_TAR_FILE" | tee -a $LOG
echo "Command: $TAR -xzvf $TAG_TAR_FILE -C $TAG_DIR --strip-components 1"
$TAR -xzvf $TAG_TAR_FILE -C $TAG_DIR --strip-components 1

#Remove the tar file
rm -f $TAG_TAR_FILE

date
echo "Program complete"

