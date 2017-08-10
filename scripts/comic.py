#!/usr/local/bin/python3

import os,sys
import pdb
import zipfile
import optparse
try:
    import magic
except:
    print("[Warning] No magic library inputed some ferature not woking properly")
from subprocess import call

class Comic:

    def __init__(self):
        self.images = ("jpg","jpeg","png","tiff","gif","bmp")
        self.archives = ('cbr','cbz','cb7','zip')
        self.incompatible = set()#.DS_store eg

        parser = optparse.OptionParser()
        parser.add_option('-n','--name',dest='name',help='Set name to name for inputed file')
        parser.add_option('-d','--dir',dest='target_path',help='Set path for directory where to save file',default='./')
        parser.add_option('-e','--extention',dest='extention',help='Set which exetentsion should be converted', default="cbz")#nargs='*'
        #parser.add_option('-t',dest='trash',help='Trash file after convertion',action='store_true',default=False)
        parser.add_option('-c',dest='clean',help='File name without empty characters',action='store_true',default=False)
        parser.add_option('-v',dest='verbose', help='Verbose output', action='store_true', default=False)
        (self.options, self.args) = parser.parse_args()
        self.reset_settings()

        if self.options.extention not in self.archives:
            sys.exit("Not supported extension")

        if self.args:
            for arg in self.args:
                self.search_file(arg)
                self.zip_archive(self.fix_input_n(arg))
                self.reset_settings()
                print("\nNot compatible files:{}".format(','.join([inc for inc in self.incompatible])))
            #call("trash " + os.path.abspath(trasher.replace(' ','\ ').replace(')','\)').replace('(','\(')),shell=True) 
        else:
            parser.print_help()

    def fix_input_n(self,input_file):
        if not self.options.name:
            def_name = input_file[:-1] if input_file.endswith('/') else input_file
            return ''.join(def_name.split('/')[-1])
        return self.options.name

    def reset_settings(self):
        self.number = 0
        self.index = 1
        self.dict = {}

    def recognize_file(self,file_):
        try:
            return magic.from_file(file_,mime=True).replace('image/','')
        except:
            return file_.split('.')[-1].lower()

    def search_file(self,if_name):

        def test_file(file_,folder):
            return os.path.isfile(os.path.join(folder,file_)) and self.recognize_file(file_) in self.images

        for input_ in os.listdir(if_name):
            testDir = os.path.join(os.path.abspath(if_name),input_)
            if os.path.isdir(testDir):
                search_file(testDir,self.dict)
            else:
                if test_file(input_,if_name):
                    os.chmod(os.path.join(if_name,input_),436)
                    self.number += 1
                    type_ = self.recognize_file(os.path.join(if_name,input_))
                    self.dict[self.number] = [input_, os.path.expandvars(os.path.realpath(if_name)) if self.options.target_path == "./" else self.options.target_path, type_]
                else:
                    if input_ not in self.incompatible:
                        self.incompatible.add(input_)

    def zip_archive(self,file_name):

        def flush_print(what):
            sys.stdout.write(what)
            sys.stdout.flush()

        def shorte(word):
            return word if len(word) < 7 else "_{}".format(word[-7:])

        def clean_name(name):
            return name.replace(" ",'_') if self.options.clean else name

        path = self.options.target_path if self.options.target_path.endswith('/') else self.options.target_path + '/'
        if self.dict:
            comp_f = zipfile.ZipFile("{}{}.{}".format(path,
                clean_name(file_name),self.options.extention),'w')
            for dic in self.dict:
                flush_print("\rAdding %8s ( %s of %s) to %s" %
                        (shorte(self.dict[dic][0]),'{0:0>3}'.format(self.index),len(self.dict),file_name))
                comp_f.write('{}/{}'.format(self.dict[dic][1],self.dict[dic][0]),
                        '{}/{}{}.{}'.format(file_name,file_name,'_{0:0>3}'.format(dic),self.dict[dic][2]))
                if self.options.verbose:
                    print('{}/{}'.format(self.dict[dic][1],self.dict[dic][0]),
                            '{}/{}{}.{}'.format(file_name,file_name,'_{0:0>3}'.format(dic),self.dict[dic][2]))

                self.index += 1
            comp_f.close()

if __name__ == "__main__":
    comic = Comic()
