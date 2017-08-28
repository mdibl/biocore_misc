# -*- coding: utf-8 -*-

from biocore_config import BiocoreDOM
from data_download_log_dom import DownloadsLogDOM
from xml.etree.ElementTree import Element
import sys,json
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
    '''
    Turns a log object into a dictionary
    '''
    def log_object_to_dict(self,logObject):
        logDict={}
        logDict["name"]=logObject.source_name
        logDict["version"]=logObject.version
        logDict["dataset"]=logObject.dataset
        logDict["download_starts"]=logObject.download_start_date
        logDict["download_ends"]=logObject.download_end_date
        logDict["remote_site"]=logObject.remote_site
        logDict["remote_directory"]=logObject.remote_directory
        logDict["remote_files"]=logObject.remote_files
        logDict["local_directory"]=logObject.local_directory
        logDict["wget_log_file"]=logObject.wget_log_file
        return logDict
        
    ##
    # convert log object to xml element and returns the xml string
    #
    def log_object_to_xml(self,tag,logObject):
        xml_elem = Element(tag)
        for key,val in self.log_object_to_dict(logObject).items():
            xml_elem_child= Element(key)
            if "remote_files" in key: val=','.join(val)
            xml_elem_child.text=str(val)
            xml_elem.append(xml_elem_child)
        return xml_elem
    
    '''
    def log_object_to_xml(self,logObject):
        xml_string="<source name='"+logObject.source_name+"'>\n"
        xml_string+="<version>"+logObject.version+"</version>\n"
        xml_string+="<dataset>"+logObject.dataset+"</dataset>\n"
        xml_string+="<download_starts>"+logObject.download_start_date+"</download_starts>\n"
        xml_string+="<download_ends>"+logObject.download_end_date+"</download_ends>\n"
        xml_string+="<remote_site>"+logObject.remote_site+"</remote_site>\n"
        xml_string+="<remote_directory>"+logObject.remote_directory+"</remote_directory>\n"
        xml_string+="<remote_files>"+','.join(logObject.remote_files)+"</remote_files>\n"
        xml_string+="<local_directory>"+logObject.local_directory+"</local_directory>\n"
        xml_string+="<wget_log_file>"+logObject.wget_log_file+"</wget_log_file>\n"
        xml_string+="</source>\n"
        return  xml_string
    '''
    ##
    # convert log object to json object and returns the json string
    #
    def log_object_to_json(self,logObject):
        return  json.dumps(self.log_object_to_dict(logObject))
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
                 print myLogDAO.log_object_to_json(logObject)

