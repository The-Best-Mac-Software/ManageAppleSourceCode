import urllib
import argparse
import re
import ConfigParser
from TouchWeb import TouchWeb

# def getHtml(url):
#     page = urllib.urlopen(url)
#     html = page.read()
#
#     return html

# html = getHtml("http://tieba.baidu.com/p/2738151262")
#
# print html

#read config
def check_args(args):

    print args["os_version"]
    print args["config_path"]

    #1. check the  value
    if(not args["os_version"] or not args["config_path"]):
        return -1
    #2.
    # os_version = re.compile(r'\d{2}\.\d{0,2}.*')
    # match = os_version.match(args["os_version"])
    # if not match:
    #     print "here"
    #     return -1

    #3. rewrite the osx version, remove all ".", just leave numbers
    os_version = args["os_version"].strip()
    os_version = os_version.replace('.', '')
    args["os_version"] = os_version

    return 0

def parse_config(args):
    conf = ConfigParser.ConfigParser()
    conf.read(args["config_path"])

    return conf

def get_config_value(config, section, node):
    if(not section or not node or not config):
        return None

    return config.get(section, node)

#parse args
def parse_opt():
    parser = argparse.ArgumentParser()

    parser.description = "manager apple"
    parser.add_argument("-o", "--osversion", dest="os_version", required=True, default="10.11.1")
    parser.add_argument("-c", "-confg", dest="config_path", required=True, default="./config.ini")

    return vars(parser.parse_args())


if __name__ == "__main__":
    #1. get option cell
    args = parse_opt()

    #2. check args
    if(check_args(args)==-1):
        print("args failed")
        exit(-1)

    #3. get arch
    arch = args["os_version"]
    config = args["config_path"]

    #4. read config file and object
    config = parse_config(args)
    weburl = get_config_value(config, "arg", "weburl")

    #5. parse web
    web_touch = TouchWeb(weburl, args, config)
