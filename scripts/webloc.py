#!/usr/local/bin/python3
import sys,os
import optparse
import re
from xml.etree import ElementTree as ET

class Webloc:

    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option('-n',dest='name',help='Name what webloc file should have')
        parser.add_option('-l',dest='long_link',help='Use long URL link',action='store_true',default=False)
        parser.add_option('-r',dest='read_webloc',help='Read webloc file',action='store_true',default=False)
        parser.add_option('-p',dest='not_exec',help='Just print the final result',action='store_true',default=False)
        (self.options, self.args) = parser.parse_args()

        self.myHash = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>URL</key>
    <string>%s</string>
</dict>
</plist>"""

        # I am reading file or just writing (could be better)
        if self.args and not all([self.options.read_webloc, self.options.long_link, self.options.name]):
            for arg in self.args:
                if not self.options.read_webloc:
                    self.create_file(arg.replace('&',"&amp;"))
                elif self.options.read_webloc:
                    self.read_file(os.path.realpath(arg))
        else:
            print("Wrong/empty input try again")

    def create_file(self, arg_name):
        if self.options.name:
            with open(os.path.abspath('./') + "/" + self.options.name + ".webloc", 'w') as f:
                f.write(self.myHash % arg_name)
        elif not self.options.not_exec:
            with open(os.path.abspath('./') + "/" + self.get_name(arg_name) + ".webloc", 'w') as f:
                f.write(self.myHash % arg_name)
        else:
            print(self.get_name(arg_name))

    def read_file(self, fileWithPath, data = ""):
        if os.path.exists(fileWithPath):
            with open(fileWithPath,'r') as file:
                data = [x for x in file.readlines() if 'string' in x][0].strip()
        print(ET.fromstring(data).text)

    def get_name(self, link):
        shortcut = re.sub('http(s)?://','',link).replace('www.','').split('.')
        if not self.options.long_link:
            return shortcut[0]
        else:
            return shortcut[0] + '-' + sorted([x for x in shortcut[1].split('/') if len(x) >= 5],key=len,reverse=True)[0]

if __name__ == "__main__":
    webloc = Webloc()

