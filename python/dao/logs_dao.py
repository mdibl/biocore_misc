# -*- coding: utf-8 -*-

from biocore_config import BiocoreDOM
from os import listdir
from os.path import isfile, isdir,join

'''
#
# Defines actions on the members current_external_sources
# that stores the list of current external sources
# getAnnotations.sh.source.version.dataset.log
'''
 
class LogDAO(BiocoreDOM):
    def __init__(self):
        BiocoreDOM.__init__(self)
        self.current_sources=[d for d in listdir(self.external_data_dir) if isdir(join(self.external_data_dir,d))] 
    
    #
    ## Returns a list of log files generated from this source downloads
    #
    def get_logs(self,source):
        tokens= [f for f in listdir(self.data_downloads_log_dir) if isfile(join(self.data_downloads_log_dir,f))]
        target_logs=[]
        for log_file in tokens:
            if source in log_file: target_logs.append(log_file)

        return target_logs

if __name__== "__main__":
    myLogDAO=LogDAO()
    source="ensembl"
    ensembl_logs=myLogDAO.get_logs(source)
    for log in ensembl_logs:
        print(log)

