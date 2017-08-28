# -*- coding: utf-8 -*-

from os.path import isfile

'''
#
# Defines a data structure to store 
# the log generated from getAnnotations.sh script
# The log file name  format is:
# getAnnotations.sh.source.version.dataset.log

Each log file generated from running the download
script has the following information:

1. Data source name
2. Start Date
3. Source Release
4. Dataset
5. Remote site
6. Remote directory
7. Remote files
8. Local directory
9. Log file generated by wget
10. End Date

'''
class DownloadsLogDOM:
   def __init__(self,source_name,log_file):
       self.source_name=""
       self.dataset=""
       self.download_start_date=""
       self.download_end_date=""
       self.version=""
       self.remote_site=""
       self.remote_directory=""
       self.remote_files=[]
       self.local_directory=""
       self.wget_log_file=""
       if source_name in log_file:
           self.source_name=source_name
           self.set_log_dom(log_file)

   ##
   #
   def set_log(self,block):
        for token in block:
            if not ":" in token:continue
            tokens=token.split(":")
            if len(tokens)<2:continue
            if "Start Date:" in token:self.download_start_date= token
            elif "End Date:" in token:self.download_end_date= token
            elif "Release:" in token:self.version=tokens[1].lstrip(" ") 
            elif "Dataset:" in token:self.dataset=tokens[1].lstrip(" ") 
            elif "Remote site:" in token:self.remote_site=tokens[1] 
            elif "Remote directory:" in token:self.remote_directory=tokens[1] 
            elif "Local directory:" in token:self.local_directory=tokens[1] 
            elif "log:" in token:self.wget_log_file=tokens[1] 
   ##
   ##
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
                        if "Remote files:" in block:self.remote_files=block
                        else:
                            self.set_log(block)  
                        block=[]
                if len(block)>0:
                    self.set_log(block)
                    block=[]
            except:
                raise
