#!/usr/bin/env python

import os
import sys
import shutil

trash = "/Users/Ales/.Trash/"

def report(what,file_):
	print "Moving %4s:\t%s to trash" % (what,file_)

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
			num = 0
			case = 0
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
	else:
		print "File %s not found" % (os.path.basename(from_))

if __name__ == "__main__":
	if len(sys.argv[1:]) > 0:
		arguments = sys.argv[1:]
		for file_ in arguments:
			if os.path.isdir(os.path.abspath(file_)):
				report("folder",file_)
			else:
				report("file",file_)
			move(os.path.abspath(file_),trash,os.path.basename(file_))
	else:
		 print "No input\nexample: trash /path/to/file.txt"

