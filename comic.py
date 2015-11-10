#!/usr/bin/env python

import os
import sys
import zipfile

images = ["jpg","jpeg","png","tiff","bmp"]

def testFile(file_):
	if os.path.isfile(file_) and file_[:-3].lower() in images:
		return True
	else:
		return False

def seraching(directory):
	list_ = []
	for dir_ in directory:
		if testFile(dir_):
			list_.add(dir_)	 
		else:
			seraching(dir_)
	return list_

def archive(list_):
	
# Coping image (1 of 100) to filenam1.cbr 	
# Coping image (22 of 67) to filenam2.cbr

if __name__ == "__main__":
	if sys.argv[1] == "mode":
		print "Entering comic mode..."
		what = True
		volume = 0
		print "Current Volume is " + str(volume) + " what is your order?"
		while what:
			order = raw_input('Next[N],Previos[P],Status[S],Reset[R],End[E]: ')
			if order == "N" or order == "n":
				volume += 1
				os.system("open -a DrawnStrips\ Reader ./*%s.cbr" % (volume))
			elif order == "P" or order == "p":
				volume -= 1
				os.system("open -a DrawnStrips\ Reader ./*%s.cbr" % (volume))
			elif order == "S" or order == "s":
				print "Your current volume is " + str(volume)
				os.system("ls -lh")
			elif order == "E" or order == "e":
				what = False
			elif order == "R" or order == "r":
				print "Reseting from %s to 0" % (volume)
				volume = 0
			else:
				print "Wrong input.."
	else:
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

