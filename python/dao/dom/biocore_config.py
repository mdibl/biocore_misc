# -*- coding: utf-8 -*-

from os import listdir
from os.path import join,isdir,isfile

class BiocoreDOM:
    def __init__(self):
        self.external_data_dir="/data/external"
        self.internal_data_dir="/data/internal"

        self.external_software_dir="/opt/software/external"
        self.internal_software_dir="/opt/software/internal"
   
        self.log_dir="/data/logs"
        self.data_downloads_log_dir="/data/logs/data_downloads"
        
        self.data_downloads_scripts_dir="/usr/local/biocore/data_downloads"
        self.current_sources=[]
        self.current_logs= []
        self.set_biocore()
 
    def set_biocore(self):
        if isdir(self.external_data_dir):
            self.current_sources=[d for d in listdir(self.external_data_dir) if isdir(join(self.external_data_dir,d))]
        if isdir(self.data_downloads_log_dir):
            self.current_logs= [f for f in listdir(self.data_downloads_log_dir) if isfile(join(self.data_downloads_log_dir,f))]
