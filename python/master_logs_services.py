# -*- coding: utf-8 -*-

from dao.logs_dao import LogDAO
from shutil import copyfile
from os.path import isfile
from xml.etree.ElementTree import tostring

'''
Uses actions define in LogDAO to generate 
  master log files containing downloads info for
all source. The files are generated in both
xml and json formats 

'''
class MasterLogServices(LogDAO):
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
        fh.close()
    
    def gen_master_xml_file(self):
        if isfile(self.data_downloads_log_xml):
           old_file=self.data_downloads_log_xml+".old"
           copyfile(self.data_downloads_log_xml, old_file)
        fh=open(self.data_downloads_log_xml,'w')
        tokens=[]
        for source in self.current_sources:
            target_logs=self.get_logs(source)
            for version in target_logs:
                for log_file in target_logs[version]:
                     logObject=self.get_log_object(source,log_file)
                     tokens.append(tostring(self.log_object_to_xml("source",logObject)))
        xml_string="<?xml version='1.0' encoding='utf-8'?>\n"
        xml_string+="<sources>\n"+"\n".join(tokens)+"\n</sources>"
        fh.write(xml_string)
        fh.close()
        
if __name__== "__main__":
    mLogs=MasterLogServices()
    mLogs.gen_master_json_file()
    mLogs.gen_master_xml_file()
