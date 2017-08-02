#!/bin/sh

JENKINS_BASE=/opt/software/external/jenkins
JENKINS_HOME=$JENKINS_BASE/.jenkins
JAVA=`which java`

export JENKINS_HOME

cd $JENKINS_BASE
nohup $JAVA -jar jenkins.war --httpPort=10080 -XX:MaxPermSize=512m &

exit 0
