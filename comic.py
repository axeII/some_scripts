#!/usr/local/bin/python

import os
import sys
import zipfile

folders = sys.argv[1:]

for folder in folders:
	files = os.listdir(folder)
	name = os.path.basename(folder) + ".cbr"
	f = zipfile.ZipFile("./" + name,"w")
	for file_ in files:
		fileName = os.path.abspath(folder) + "/" + file_
		print "Adding %s  to  %s" % (fileName, name)
		f.write(fileName)
	f.close()

