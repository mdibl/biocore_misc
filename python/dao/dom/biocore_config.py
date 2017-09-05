# -*- coding: utf-8 -*-

from os import listdir
from os.path import join,isdir,isfile
import xml.etree.ElementTree as ET

'''
A base class that sets the path to biocore info  
'''
class BiocoreDOM:
    def __init__(self):
        self.external_data_dir="/data/external"
        self.internal_data_dir="/data/internal"

        self.external_software_dir="/opt/software/external"
        self.internal_software_dir="/opt/software/internal"
   
        self.log_dir="/data/logs"
        self.data_downloads_log_dir="/data/logs/data_downloads"
        self.data_downloads_log_json=self.data_downloads_log_dir+"/master_log.json"
        self.data_downloads_log_xml=self.data_downloads_log_dir+"/master_log.xml"
        self.data_downloads_log_html=self.data_downloads_log_dir+"/master_log.html"
        
        self.data_downloads_scripts_dir="/usr/local/biocore/data_downloads"
        
        self.current_sources=[]
        self.current_external_software=[]
        self.current_logs= []
        self.set_biocore()
        
        self.logFieldLabel={}
        self.logFieldLabel["name"]="Source Name"
        self.logFieldLabel["version"]="Version"
        self.logFieldLabel["dataset"]="Dataset"
        self.logFieldLabel["download_starts"]="Download Started"
        self.logFieldLabel["download_ends"]="Donload Ended"
        self.logFieldLabel["remote_site"]="Remote Site"
        self.logFieldLabel["remote_directory"]="Remote Path To Data"
        self.logFieldLabel["remote_files"]="Remote Files"
        self.logFieldLabel["local_directory"]="Local Path To Data"
        self.logFieldLabel["wget_log_file"]="Local Path To Logs"
 
    def set_biocore(self):
        if isdir(self.external_data_dir):
            self.current_sources=[d for d in listdir(self.external_data_dir) if isdir(join(self.external_data_dir,d))]
        if isdir(self.data_downloads_log_dir):
            self.current_logs= [f for f in listdir(self.data_downloads_log_dir) if isfile(join(self.data_downloads_log_dir,f))]
    
    def getXmlDocRoot(self,xml_file):
        doc_root=None
        if not isfile(xml_file): 
            print("File does not exist "+xml_file )
            return doc_root
        try:
            xml_doc=ET.parse(xml_file)
            doc_root=xml_doc.getroot()
        except:pass
        return doc_root
