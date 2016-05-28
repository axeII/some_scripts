#!/usr/bin/env python

import os,sys
from termcolor import colored
import shutil

def setTrash():
    try:
        trash = os.environ['TRASH'] + '/'
        return trash 
    except KeyError:
        print   "Local trash file is not set. Check your enviroment settings"
        setEnviroment(raw_input('Do you want to set localTrash? [Y/N]'))
        sys.exit(12)

trash = setTrash()

def setEnviroment(answer):
    if answer.lower() in ('yes','y'):
        with os.environ['HOME'] + "/.Trash" as directory:
            if not os.path.isdir(directory):
                os.makedirs(directory)
            with open(os.environ['HOME']+'.bashrc','a') as locFile:
                locFile.write('export TRASH=\"$HOME/.Trash\"')

def report(name):
	if (os.path.isdir(trash+os.path.basename(name))):
		what = "Folder"
	else:
		what = "File  "	 
	print "\t%s\t%s" % (colored(what,'blue'),colored(name,'green'))

def fileExists(what):
	return os.path.exists(os.path.abspath(what))

def testChar(char,name):
	return char in name

def fixCase(which,what):
	if which >= 1:
		what = what[:-2]
	return what	

def move(from_,position,name):
	if fileExists(from_):
		if fileExists(name):
			num = case = 0
			while os.path.exists(position+name):
				num += 1
				if testChar('.',name):
					end = name.split(".")[-1]
					begin = ".".join(name.split(".")[:-1])
					name = fixCase(case,begin) + "-" + str(num) + "." + str(end)
				else:
					name = fixCase(case,name) + "-" + str(num)
				case += 1
		shutil.move(from_,position+name)
		return True
	else:
		return False

if __name__ == "__main__":
	if len(sys.argv[1:]) > 0:
		arguments = sys.argv[1:]
		print "Moving to trash: \n"
		for file_ in arguments:
			original = os.path.abspath(file_)
			status = move(os.path.abspath(file_),trash,os.path.basename(file_))
			if status:
				report(original)		
			else:
				print colored("\tError   %s not found in this directory: %s",'red') % (colored(os.path.basename(file_),'blue'),colored(os.path.dirname(os.path.abspath(file_)),'red'))

	else:
		 print "No input\nexample: trash /path/to/file.txt"

