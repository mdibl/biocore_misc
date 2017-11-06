# -*- coding: utf-8 -*-

from dao.package_downloads_logs_dao import PackageLogDAO
from shutil import copyfile
from os.path import isfile

'''
Uses actions define in PackageLogDAO to generate 
master log files containing Package downloads info for
all packages. The files are generated in
html, xml and json formats 

'''
class MasterLogServices(PackageLogDAO):
    def __init__(self):
        PackageLogDAO.__init__(self)     
        self.data_downloads_log_json=self.external_software_dir+"/package_master_log.json"
        self.data_downloads_log_xml=self.external_software_dir+"/package_master_log.xml"
        self.data_downloads_log_html=self.external_software_dir+"/package_master_log.html"
        
    def gen_master_json_file(self):
        if isfile(self.data_downloads_log_json):
           old_file=self.data_downloads_log_json+".old"
           copyfile(self.data_downloads_log_json, old_file)
        fh=open(self.data_downloads_log_json,'w')
        tokens=[]
        for package in self.current_external_software:
            target_logs=self.get_logs(package)
            if len(target_logs)<=0:continue
            for log_file in target_logs:
                 logObject=self.get_log_object(log_file)
                 tokens.append(self.log_object_to_json(logObject))
        json_string='{"packages":'+",\n".join(tokens)+"}"
        fh.write(json_string)
        fh.close()
    
    def gen_master_xml_file(self):
        if isfile(self.data_downloads_log_xml):
           old_file=self.data_downloads_log_xml+".old"
           copyfile(self.data_downloads_log_xml, old_file)
        fh=open(self.data_downloads_log_xml,'w')
        tokens=[]
        for package in self.current_external_software:
            target_logs=self.get_logs(package)
            if len(target_logs)<=0:continue
            for log_file in target_logs:
                 logObject=self.get_log_object(log_file)
                 tokens.append("\n".join(self.log_object_to_xml_string("package",logObject)))
        xml_string="<?xml version='1.0' encoding='utf-8'?>\n"
        xml_string+="<packages>\n"+"\n".join(tokens)+"\n</packages>"
        fh.write(xml_string)
        fh.close()
    
    def get_install_date(self,package,version):
        xmldoc_root=self.getXmlDocRoot(self.data_downloads_log_xml)
        install_date=""
        log_entries=xmldoc_root.findall("./package/[package_name='"+package+"']")
        if version is None:version=""
        for package_entry in log_entries:
            if package_entry.find("./[package_version='"+version+"']") is not None:
                install_date=package_entry.find("./install_date").text
        return install_date

        
    def gen_main_nav(self):
        nav=[]
        for source,versions in sorted(self.get_source_releases().items()):
            for version in versions:
                if version is None: version=""
                src_version=source+":"+version
                date_fields=self.get_install_date(source,version).split(' ')
                download_date=' '.join(date_fields[0:3])
                download_date+=", "+date_fields[len(date_fields)-1]
                dl="<dl class='row'><dt class='col-xs-4'><a href='#"+src_version+"'>"+src_version+"</a></dt>"
                dl+="<dd class='col-xs-8'><b>Install Date: </b> "+download_date+"</dd></dl>"
                nav.append(dl)
        return "<nav class='col-xs-12'><div class='nav-list'>"+"\n".join(nav)+"</div></nav>"     
      
    def gen_log_table(self,xml_element):
        table=[]
        version=xml_element.find("./package_version")
        package_name=xml_element.find("./package_name")
        if version is None: version=""
        src_version=package_name.text+":"+version.text
        table.append("<div class='col-xs-12 container'><a id='"+src_version+"'></a><h2>"+src_version+"</h2>")
        version_data=""
        for tag_entry in xml_element:
            version_data+="<dl class='row'><dt class='col-xs-12 col-sm-4'>"+str(tag_entry.attrib["label"])+"</dt>"
            version_data+="<dd class='col-xs-12 col-sm-8'>"+str(tag_entry.text)+"</dd></dl>"
        version_data+="<nav class='back-to-top'><a href=''>Back to top</a></nav>"
        table.append(version_data)
        table.append("</div>")
        return table

    def get_xml_element(self,package_name,doc_root,version):
        xml_element=None
        for element in self.get_log_entries(package_name,doc_root):
            if version in element.find("./package_version").text:xml_element=element
        return xml_element

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
                fh.write("\n<body><div class='container'>\n")
                fh.write("<div class='col-xs-12 container-header'><h1>External Software Packages </h1></div>\n")
                fh.write(self.gen_main_nav())
                for package,versions in sorted(self.get_source_releases().items()):
                    for version in versions:
                        if version is None: version=""
                        package_element=self.get_xml_element(package,xmldoc_root,version)
                        fh.write("\n".join(self.gen_log_table(package_element)))
                fh.write("</div></body></html>")
                fh.close()
            except:raise
    
    def get_version_list(self,source_entries):
        block=[]
        for xml_element in source_entries:
            version=xml_element.find("./package_version")
            if not version.text in block: block.append(version.text)
        return block

    def get_log_entries(self,package,doc_root):
        return doc_root.findall("./package/[package_name='"+package+"']")
    '''
     Returns a map of sources with associated versions
    '''
    def get_source_releases(self):
        packages={}
        xmldoc_root=self.getXmlDocRoot(self.data_downloads_log_xml)
        for package in self.current_external_software:
            packages[package]=self.get_version_list(self.get_log_entries(package,xmldoc_root))
        return packages

if __name__== "__main__":
    mLogs=MasterLogServices()
    print "Generating master json"
    mLogs.gen_master_json_file()
    print "Generating master xml"
    mLogs.gen_master_xml_file()
    print "Generating master html"
    mLogs.gen_master_html_file()
    
