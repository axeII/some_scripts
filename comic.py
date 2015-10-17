#!/usr/local/bin/python

import os
import sys
import zipfile

folders = sys.argv[1:]

for folder in folders:
	files = os.listdir(folder)
	f = zipfile.ZipFile(folder + ".cbr","w")
	for file_ in files:
		print "Adding %s to %s.cbr " % (file_,folder)
		f.write(os.path.abspath(folder+"/"+file_))
	f.close()
	
