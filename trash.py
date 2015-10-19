#!/usr/local/bin/python

import os
import sys
import shutil

arguments = sys.argv[1:]
path_ = os.path.abspath("./")

def report(what,file_):
	print "Moving %6s: %6s to trash" % (what,file_)

def move(from_,to_):
	number = 0
	name = to_
	while os.path.exists(to_):
		number += 1
		if not os.path.exists(to_+str(number)):
			name = to_+str(number)
			break

	shutil.move(from_,name)

for file_ in arguments:
	if os.path.isdir(os.path.join(path_,file_)):
		report("folder",file_)
	else:
		report("file",file_)
	move(os.path.abspath(file_),"/Users/Ales/.Trash/" + os.path.basename(file_))
