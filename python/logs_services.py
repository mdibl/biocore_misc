# -*- coding: utf-8 -*-

from dao.logs_dao import LogDAO
from shutil import copyfile

from os.path import isfile, isdir,join

'''
'''
 
class LogServices(LogDAO):
    def __init__(self):
        LogDAO.__init__(self)
        
    
    def gen_master_json_file(self):
        if isfile(self.data_downloads_log_json):
           old_file=self.data_downloads_log_json+".old"
           copyfile(self.data_downloads_log_json, old_file)
        fh=open(self.data_downloads_log_json,'w')
        tokens=[]
        for source in self.current_sources:
            target_logs=self.get_logs(source)
            for version in target_logs:
                for log_file in target_logs[version]:
                     logObject=self.get_log_object(source,log_file)
                     tokens.append(self.log_object_to_json(logObject))
        json_string='{"sources":'+",\n".join(tokens)+"}"
        fh.write(json_string)
    
if __name__== "__main__":
    myLogs=LogServices()
    myLogs.gen_master_json_file()
