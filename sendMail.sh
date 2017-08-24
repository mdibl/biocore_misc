#!/bin/sh
#
#  sendMail
###########################################################################
#
#  Purpose:  This script will send the contents of the log to each
#            recipient in the mail list.
#
#  Usage:
#
#      sendMail  subject log_file
#
#      where
#
#          subject = the text to be appended to the email subject line
#
#  Env Vars:
#
#      MAIL_LIST - jenkins env variable that contains a list of email
#                  addresses to send the mail to
#
#      NODE_NAME - jenkins environment variable that contains the name of
#                  the current server where the project is running
#
#  Inputs:  subject, log_file
# 
#  Assumes: Job runs on Jenkins
#
#  Exit Codes:
#
#      0:  Successful completion
#      1:  Fatal error occurred
#
###########################################################################

if [ $# -ne 2 ]
then
    echo "Usage: $0 subject log_file"
    exit 1
fi
SUBJECT="$1"
LOG_FILE=$2

#
# Make sure the log file exists.
#
if [ ! -d "${LOG_FILE}" ]
then
    echo "The logfile ($LOG_FILE) does not exist on this server ($NODE_NAME)"
    exit 1
fi

#
# Notify admin with the contents of the log
#
mailx -s "From:${NODE_NAME} - ${SUBJECT}" ${MAIL_LIST} < "${LOG_FILE}"

exit 0
