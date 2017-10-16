# -*- coding: utf-8 -*-

from dom.biocore_config import BiocoreDOM
from dom.package_download_log_dom import PackageDownloadsLogDOM
from xml.etree.ElementTree import Element
import sys,json
from os import listdir
from os.path import isfile, isdir,join

'''

 Defines actions on logs generated from package downloads 
 using the info in runDownloadGitRepos.sh*
 and runDownloadPackage.sh* log files
'''
 
class PackageLogDAO(BiocoreDOM):
    def __init__(self):
        BiocoreDOM.__init__(self)
        
    
    '''
     Returns the object representation of data in the specified log file
    '''
    def get_log_object(self,log_file):
        return PackageDownloadsLogDOM(log_file)

    '''
    Turns a log object into a dictionary
    '''
    def log_object_to_dict(self,logObject):
        logDict={}
        logDict["package_name"]=logObject.package_name
        logDict["package_version"]=logObject.package_version
        logDict["install_date"]=logObject.install_date
        logDict["remote_site"]=logObject.remote_site
        logDict["install_directory"]=logObject.install_directory
        logDict["path_to_logs"]=logObject.path_to_logs
        logDict["git_organization"]=logObject.git_organization
        logDict["git_repos"]=logObject.git_repos
        logDict["git_url"]=logObject.git_url

        return logDict
        
    '''
     Turns log object into xml element and returns the xml element.
     It calls log_object_to_dict.
    '''
    def log_object_to_xml_element(self,tag,logObject):
        xml_elem = Element(tag)
        for key,val in self.log_object_to_dict(logObject).items():
            xml_elem_child= Element(key)
            xml_elem_child.text=str(val)
            xml_elem.append(xml_elem_child)
        return xml_elem
    
    '''
     Turns log object into xml string and returns the xml string.
     It calls log_object_to_dict.
    '''
    def log_object_to_xml_string(self,tag,logObject):
        xml_string =[]
        xml_string.append("<"+tag+">")
        for key,val in self.log_object_to_dict(logObject).items():
            label=' label="'+self.package_log_labels[key]+'"'
            xml_string.append("<"+key+label+"><![CDATA["+str(val)+"]]>"+"</"+key+">")
        xml_string.append("</"+tag+">")  
        return xml_string
       
    '''
     Turns log object into json object and returns the json string
    '''
    def log_object_to_json(self,logObject):
        return  json.dumps(self.log_object_to_dict(logObject))
    
