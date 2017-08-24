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

'''
class AnnotationLogDOM:
   def __init(self,source_name,log_file):
       self.source_name=source_name
       self.dataset=""
       self.download_date=""
       self.version=""
       self.remote_site=""
       self.remote_directory=""
       self.remote_files=[]
       self.local_directory=""
       self.wget_log_file=""
       if source_name in log_file:
           self.source_name=source_name
           self.set_log_dom(log_file)

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
                            for token in block:
                                 if not ":" in token:continue
                                 tokens=token.split(":")
                                 if len(tokens)<2:continue
                                 if "Start Date:" in token:self.download_date=join("").tokens[1:end] 
                                 else if "Release:" in token:self.version=tokens[1] 
                                 else if "Remote site:" in token:self.remote_site=tokens[1] 
                                 else if "Remote directory:" in token:self.remote_directory=tokens[1] 
                                 else if "Local directory:" in token:self.local_directory=tokens[1] 
                                 else if "log:" in token:self.wget_log_file=tokens[1] 
                        block=[]
      
            except:pass
