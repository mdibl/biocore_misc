# -*- coding: utf-8 -*-

from dao.logs_dao import LogDAO
from shutil import copyfile
from os.path import isfile

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
                     tokens.append("\n".join(self.log_object_to_xml_string("source",logObject)))
        xml_string="<?xml version='1.0' encoding='utf-8'?>\n"
        xml_string+="<sources>\n"+"\n".join(tokens)+"\n</sources>"
        fh.write(xml_string)
        fh.close()
    
    def gen_main_nav(self):
        nav=[]
        sources=self.get_source()
        for source,versions in self.get_source().items():
            for version,datasets in versions.items():
                nav.append("<li class='list-group-item'><a href='#"+source+""+version+"'>"+source:version+"</a></li>")
        return "<nav class='col-xs-12'><ul>"+"\n".join(nav)+"</ul></nav>"     
      
    def gen_log_table(self,source,source_block):
        table=[]
        for version,datasets in source_block.items():
            if version is None: version=""
            datasets_nav="<nav>"
            table.append("<div class='col-xs-12 container'><h2>"+source+":"+version+"</h2>")
            version_data=""
            for dataset,data in datasets.items():
                datasets_nav+="<a href='#"+dataset+"'>"+dataset+" | </a>"
                version_data+="<div class='col-xs-12 dataset'><a id='"+dataset+"'></a><h4>"+dataset+"</h4>"
                for label,val in sorted(data.items()):
                    if val is None:val=""
                    version_data+="<dl class='row'><dt class='col-xs-12 col-sm-4'>"+label
                    if "Remote Files" in label:
                        file_list=val.split(",")
                        files_ul="<ol>"
                        for token in file_list: files_ul+="\n<li class='list-group_item'>"+token+"</li>"
                        files_ul+="</ol>"
                        val=files_ul
                    version_data+="</dt><dd class='col-xs-12 col-sm-8'>"+val+"</dd></dl>"
                version_data+="</div>"
            table.append(datasets_nav+"</nav>")
            table.append(version_data)
            table.append("</div>")
        return table

    def get_version_block(self,source_entries):
        block={}
        for dataset_xml_element in source_entries:
            version=dataset_xml_element.find("./version")
            dataset=dataset_xml_element.find("./dataset")
            if not version.text in block: block[version.text]={}
            if not dataset.text in block[version.text]: block[version.text][dataset.text]={}
            for node in dataset_xml_element:
                label=node.attrib['label']
                block[version.text][dataset.text][label]=node.text

        return block
        
    def gen_master_html_file(self):
        if not isfile(self.data_downloads_log_xml):self.gen_master_xml_file()
        xmldoc_root=self.getXmlDocRoot(self.data_downloads_log_xml)
        if xmldoc_root is not None:
            if isfile(self.data_downloads_log_html):
                old_file=self.data_downloads_log_html+".old"
                copyfile(self.data_downloads_log_html, old_file)
            try:
                fh=open(self.data_downloads_log_html,"w")
                fh.write("<!DOCTYPE html>\n<html>\n")
                fh.write("<head>\n")
                fh.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/css/bootstrap.min.css">')   
                fh.write("\n"+'<link href="https://fonts.googleapis.com/css?family=Droid+Serif:400,700|Lato:400,700" rel="stylesheet">')
                fh.write("\n"+'<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css">')
                fh.write("\n"+'<link rel="stylesheet" href="/css/style.css">')
                fh.write("\n</head>")
                fh.write("\n<body>\n")
                fh.write(self.gen_main_nav())
                for source in self.current_sources:
                    log_entries=xmldoc_root.findall("./source/[name='"+source+"']")
                    source_block=self.get_version_block(log_entries)
                    fh.write("\n".join(self.gen_log_table(source,source_block)))
                fh.write("</body></html>")
                fh.close()
            except:raise
if __name__== "__main__":
    mLogs=MasterLogServices()
    mLogs.gen_master_json_file()
    mLogs.gen_master_xml_file()
    mLogs.gen_master_html_file()
    
