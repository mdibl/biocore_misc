# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile,join,dirname

'''

 Defines a data structure to store 
 the log generated from runDownloadGitRepos.sh
 and runDownloadPackage.sh  scripts used to
 install new software packages

 The log file name  format is:
 scriptName.package.version.log

Each log file generated from running the download
script has the following information:

1. Package/Repos name
2. Package version
3. Remote site
4. Install directory
5. Install Date
6. Path to logs
7. Git Organization
8. Git Repos

Example:
Package: bamtools
Version: v2.4.1
Install directory: /opt/software/external/bamtools
Path to Install logs: /data/logs/package_downloads
Install Date:Thu Oct 5 15:40:14 EDT 2017
Git Organization:pezmaster31
Git Repos:bamtools
'''
class PackageDownloadsLogDOM:
   def __init__(self,log_file):
       self.package_name=""
       self.install_date=""
       self.package_version=""
       self.remote_site=""
       self.install_directory=""
       self.install_dir=""
       self.path_to_logs=""
       self.git_organization=""
       self.git_repos=""
       self.git_url=""

       self.set_log_dom(log_file)

   def set_log(self,block):
        for token in block:
            if not ":" in token:continue
            try:
                tokens=token.split(":")
                if len(tokens)<2:continue
                if "Install Date:" in token:self.install_date=token.replace("Install Date:","")
                elif "Package:" in token:self.package_name=tokens[1].lstrip(" ") 
                elif "Version:" in token:self.package_version=tokens[1].lstrip(" ") 
                elif "Install directory:" in token:self.install_directory=tokens[1].lstrip(" ") 
                elif "Remote site:" in token:self.remote_site=token.replace("Remote site:","") 
                elif "Path to Install logs:" in token:self.path_to_logs=tokens[1] 
                elif "Git Organization:" in token:self.git_organization=tokens[1]
                elif "Git Repos:" in token:self.git_repos=tokens[1]
                elif "Git url:" in token:self.git_url=token.replace("Git url:","")
            except:raise
  
   def set_log_dom(self,log_file):   
        if isfile(log_file):
            try:
                fh=open(log_file,'r')
                block=[]
                for line in fh:
                    line=line.rstrip('\n')
                    if not "==" in line:block.append(line)
                    else:
                        if len(block)<=0:continue
                        self.set_log(block)  
                        block=[]
                if len(block)>0:
                    self.set_log(block)
                    block=[]
            except:
                raise

if __name__=="__main__":
    logs_base="/data/logs/package_downloads"
    log_prefix="runDownload"
    log_files=[f for f in listdir(logs_base) if isfile(join(logs_base,f))]
    for log_file in log_files:
        if not log_prefix in log_file: continue
        log_file=join(logs_base,log_file) 
        package=PackageDownloadsLogDOM(log_file)
        print "****************************"
        print "Package Name:",package.package_name
        print "****************************"
        print "Log file:",log_file
        print "Package Version:",package.package_version
        print "Install Directory:",package.install_directory
        print "Install Date:",package.install_date
        print "Path to Install logs:",package.path_to_logs
        print "Git Organization:",package.git_organization 
        print "Git Repos:",package.git_repos 
        print "Git Url:",package.git_url 
        print "Remote Site:",package.remote_site 
