#!/usr/bin/python

import os
import sys
import shutil
import optparse
import os.path as op

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    trash = os.environ['TRASH'] 
except KeyError:
    print "Local trash file is not set. Check your enviroment settings"
    sys.exit(12)

def report(argument,dir_option):
    what = "Folder " if dir_option else "File   "
    print "Info: " + bcolors.OKBLUE + what + bcolors.ENDC + bcolors.OKGREEN + argument + bcolors.ENDC

def reportError(argument):
    print bcolors.FAIL + "Erro: " + bcolors.ENDC + bcolors.OKBLUE+ op.basename(argument) + bcolors.ENDC + bcolors.FAIL + " not found in this directory: " + bcolors.ENDC + bcolors.WARNING + op.dirname((op.abspath(argument))) + bcolors.ENDC

def fixCase(which,what):
    return what[:-2] if which > 1 else what

def move(from_,position,name,dir_opt):
    if op.exists(from_):
        if op.exists(position + name):
	    num_ = case = 0
	    while op.exists(position + name):
                case = case + 1
		num_ = num_ + 1
		if op.isfile:
		    file_ = list(op.splitext(name))
		    begin = ''.join(file_[:-1])
		    name = fixCase(case,begin) + "-" + str(num_) + file_[-1]
		else:
		    name = fixCase(case,name) + "-" + str(num_)
        report(op.abspath(name),dir_opt)		
        shutil.move(from_,position+name)
    else:
        reportError(name)

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="Usage %prog [option] file/s")
    (options,args) = parser.parse_args()
    if args:
        print "Moving to trash: \n"
        for arg in args:
            file_name = op.basename(arg[:-1] if arg.endswith('/') else arg)
            is_dir = True if op.isdir(arg) else False
            move(op.abspath(arg),trash,file_name,is_dir)
    else:
        print "No input"
