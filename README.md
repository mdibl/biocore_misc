# biocore_misc

A repos to store bioadmin miscellaneous scripts 

# How to upgrade Jenkins
  * Log on to Jenkins server : jenkins.mdibl.org
  * Click on "Manage Jenkins" 
  * if there is a new release suggestion, copy the "download" link
  * ssh to lintilla
    * cd to /opt/software/external/jenkins
    * rm -f jenkins.war.bak
    * mv jenkins.war jenkins.war.bak
    * wget "http://updates.jenkins-ci.org/download/war/new_release_number/jenkins.war
     ```bash
     Example: I just upgraded from 2.60.2 to 2.60.3
     cmd: wget "http://updates.jenkins-ci.org/download/war/2.60.3/jenkins.war
     ```
  * Go back to jenkins web server
    * Click on "Manage Jenkins" (you should see the option to upgrade automatically)
    * Click on "upgrade automatically" then follow instructions 
    
