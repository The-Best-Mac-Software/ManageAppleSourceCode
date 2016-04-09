import urllib
import re
import sys
import os
import shutil

class CodeObject:
    def __init__(self, program_name, download_url):
        self.program_name = program_name
        self.download_url = download_url

    def get_program_name(self):
        return self.program_name

    def set_program_name(self, program_name):
        self.program_name = program_name

    def get_download_url(self):
        return self.download_url

    def set_download_url(self, download_url):
        self.download_url = download_url


class TouchWeb:
    def __init__(self, weburl, args, config):
        self.weburl = weburl
        self.args = args
        self.config = config
        self.work_dir = "~/10.1/"

        self.parse_url()

    def download_html_code(self, url):
        page = urllib.urlopen(url)
        return page.read()

    def download_file(self, file_name, urls):
        file = urllib.urlopen(urls)
        with open(file_name, "w+") as tar_pack:
            hex_data = file.read()
            tar_pack.write(hex_data)
            tar_pack.close()

    def view_bar(self, num=1, sum=100, bar_word=":"):
        rate = float(num) / float(sum)
        rate_num = int(rate * 100)
        print '\r%d%% :' %(rate_num),
        for i in range(0, num):
            os.write(1, bar_word)
        sys.stdout.flush()

    def parse_project(self, apple_page):
        project_row = re.compile(r"\<tr\ class=\"project-row\"\>([\s\w\<\>\"\=\\\/\.\-]+?)\<\/tr\>")
        search = re.findall(project_row, apple_page)

        if(search==None or not len(search)):
            print("there is no any source code, result is none or length is 0")
            return None

        if(os.path.exists("./source/")):
            shutil.rmtree("./source/")

        os.mkdir("./source/")

        total_source = len(search)
        counter = 0

        for single in search:
            counter+=1

            parse_a_tag = re.compile(r'\<a href\=\"[\\\w\-\/\"\.]+?\>[\<\>\=\"\/\\\.\w\d\-\s]+?\<\/a\>')
            match = re.findall(parse_a_tag, single)

            program_name = None
            url = None

            #parse source name
            if(len(match)>=1):
                first_block = match[0]
                array = first_block.split('>')
                if(array<2):
                    continue
                first_block = array[1]
                array = first_block.split('<')
                if(len(array)<1):
                    continue;

                program_name = (array[0].split())[0]
                # print program_name
            if(len(match)>=2):
                second_block = match[1]
                # print second_block
                url = second_block.split('"')[1]
                main_url = self.weburl+url
                print "prepare to download file : " + main_url
                self.view_bar(counter, total_source, "downloading "+program_name+".tar.gz")
                self.download_file("./source/"+program_name+".tar.gz", main_url)
                # print main_url



    def parse_url(self):
        if(self.weburl[-1]!='/'):
            self.weburl+='/'

        os_source_tag = (self.config.get("arg", "os_source_tag_fmt")).format(self.args["os_version"])
        print "[+] get the regex format %s " % os_source_tag

        apple_url_os = self.weburl + os_source_tag
        print apple_url_os

        apple_source_page = self.download_html_code(apple_url_os)
        # print apple_source_page
        self.parse_project(apple_source_page)




