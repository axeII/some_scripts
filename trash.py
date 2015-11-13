#!/usr/bin/env python

import os
import sys
import shutil

trash = "/Users/Ales/.Trash/"
path_ = "./"

def report(what,file_):
	print "Moving %6s: %6s to trash" % (what,file_)

def fileExists(what):
	if os.path.exists(os.path.abspath(what)):
		return True
	else:
		return False

def move(from_,to_):
	num = 0
	name = to_
	while os.path.exists(to_):
		num += 1
		end = to_.split(".")[-1]
		begin = to_.split(".")[:-1]
		orig = ".".join(begin)
		new = orig + "-" + str(num) + "." + str(end)
		if not os.path.exists(new):
			name = new
			break

	if fileExists(from_):
		shutil.move(from_,name)
	else:
		print "File %s not found" % (os.path.basename(from_))

if __name__ == "__main__":
	if len(sys.argv[1:]) > 0:
		arguments = sys.argv[1:]
		for file_ in arguments:
			if os.path.isdir(os.path.join(os.path.abspath(path_),file_)):
				report("folder",file_)
			else:
				report("file",file_)
			move(os.path.abspath(file_),trash + os.path.basename(file_))
	else:
		 print "No input\nexample: trash /path/to/file.txt"

