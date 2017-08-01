#!/bin/sh

JENKINS_BASE=/usr/local/biocore/jenkins
JENKINS_HOME=$JENKINS_BASE/.jenkins
export JENKINS_HOME
nohup /usr/bin/java -jar $JENKINS_BASE/jenkins.war --httpPort=10080 -XX:MaxPermSize=512m &
~                                                                                                                  
~        
