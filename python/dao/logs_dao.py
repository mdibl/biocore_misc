# -*- coding: utf-8 -*-

from biocore_config import BiocoreDOM
from data_download_log_dom import DownloadsLogDOM
import sys
from os import listdir
from os.path import isfile, isdir,join

'''
#
# Defines actions on logs generated from data downloads 
# using the info in getAnnotations.sh.source.version.dataset.log
'''
 
class LogDAO(BiocoreDOM):
    def __init__(self):
        BiocoreDOM.__init__(self)
    
    #
    ## Returns a list of log files generated from this source downloads
    #  stored by version whne applicable
    #
    def get_logs(self,source):
        target_logs={}
        for log_file in self.current_logs:
            if source in log_file and "getAnnotations" in log_file: 
                try:
                    tokens=log_file.split('.')
                    release=tokens[3]
                    if not release in target_logs:target_logs[release]=[]
                    target_logs[release].append(join(self.data_downloads_log_dir,log_file))
                except:
                    print("Failed because of: ",sys.exc_info()[0])
                    raise
        return target_logs
    ##
    # convert log object to xml element and returns the xml string
    #
    def log_object_to_xml(self,logObject):
        xml_string="<source name='"+logObject.source_name+"'>\n"
        xml_string+="<version>"+logObject.version+"</version>\n"
        xml_string+="<dataset>"+logObject.dataset+"</dataset>\n"
        xml_string+="<begins>"+logObject.download_start_date+"</begins>\n"
        xml_string+="<ends>"+logObject.download_end_date+"</ends>\n"
        xml_string+="<remote_site>"+logObject.remote_site+"</remote_site>\n"
        xml_string+="<remote_directory>"+logObject.remote_directory+"</remote_directory>\n"
        xml_string+="<remote_files>"+','.join(logObject.remote_files)+"</remote_files>\n"
        xml_string+="<local_directory>"+logObject.local_directory+"</local_directory>\n"
        xml_string+="<wget_log_file>"+logObject.wget_log_file+"</wget_log_file>\n"
        xml_string+="</source>\n"
        return  xml_string
    #
    # Returns an object representing data in the specified log file
    #
    def get_log_object(self,source,log_file):
        return DownloadsLogDOM(source,log_file)

if __name__== "__main__":
    myLogDAO=LogDAO()
    for source in myLogDAO.current_sources:
        target_logs=myLogDAO.get_logs(source)
        for version in target_logs:
            for log_file in target_logs[version]:
                 logObject=myLogDAO.get_log_object(source,log_file)
                 print myLogDAO.log_object_to_xml(logObject)

