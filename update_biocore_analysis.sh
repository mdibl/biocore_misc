#!/bin/bash

## What it does:
# 1) Pulls updates on local copy of a git repos from remote server
# 2) rsync /data/projects/Bicore/biocore_analysis with ~/github_repos/biocore_analysis
# 3) pushes updates if any to remote
# Runs as cron on local server
#
script_name=`basename $0`
cd `dirname $0`
working_dir=`pwd`

source ~/.bashrc

repos_name=`basename $BC_CLONE_BASE`
repos_base=`dirname $BC_CLONE_BASE`
git_repos_url=https://$GIT_TOKEN@$GIT_URL/$GIT_ORG/$repos_name.git
GIT=`which git`
#####################
LOG_DIR=$working_dir/logs

[ ! -d $LOG_DIR ] && mkdir -p $LOG_DIR

LOG=$LOG_DIR/$script_name.log
rm -f $LOG
touch $LOG

date | tee -a $LOG
echo "The path to logs is $LOG_DIR" | tee -a $LOG
echo "Repository Name : $repos_name"| tee -a $LOG
echo "Cloned Path: $BC_CLONE_BASE"| tee -a $LOG
echo "Installed under: $BC_REPOS_BASE" | tee -a $LOG

date | tee -a $LOG


####################
if [ ! -f $GIT ]
then
    echo "ERROR: git not installed on `uname -n` "
    exit 1
fi
if [ ! -d $BC_CLONE_BASE ]
then
  cd $repos_base
  $GIT clone $git_repos_url
fi
if [ ! -d $BC_CLONE_BASE ]
then
  echo "Can't clone $repos_name under $repos_base"
  exit 1
fi
## Cd to the cloned repos
cd $BC_CLONE_BASE 
$GIT pull


