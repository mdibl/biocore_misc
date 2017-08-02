#!/bin/sh

JENKINS_BASE=/opt/software/external/jenkins
JENKINS_HOME=$JENKINS_BASE/.jenkins
JAVA=`which java`

export JENKINS_HOME
nohup $JAVA -jar $JENKINS_BASE/jenkins.war --httpPort=10080 -XX:MaxPermSize=512m &
