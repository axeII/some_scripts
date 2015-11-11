#!/usr/bin/env python

import os
import sys
import zipfile

images = ["jpg","jpeg","png","tiff","bmp"]
incompatible = []

def testFile(file_,folder):
	if os.path.isfile(os.path.join(folder,file_)) and file_[-3:].lower() in images:
		return True
	else:
		return False

def serachFile(directory,dictionary):
	files = os.listdir(directory)
	for thing in files:
		if os.path.isdir(os.path.join(directory,thing)):
			 serachFile(os.path.join(os.path.abspath(directory),thing),dictionary)
		else:
			if testFile(thing,directory):
				dictionary[thing] = os.path.expandvars(os.path.realpath(directory))
			else:	
				if thing not in incompatible: incompatible.append(thing)
	return dictionary	

def printFile(fileX,nameX):
	print "Adding %s to %s " % (fileX,nameX) #flash

# Coping image (1 of 100) to filenam1.cbr 	
# Coping image (22 of 67) to filenam2.cbr

def zipArchive(name,dictionary):
	i = 0 
	f = zipfile.ZipFile("./" + name,'w')
	for dic in dictionary:
		printFile(dic,name)
		f.write(dictionary[dic]+"/"+dic)
	f.close()

def comicMode():
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

	
if __name__ == "__main__":
	if len(sys.argv[1:]) < 1:
		print "navod"
	else:
		if sys.argv[1] == "mode":
			comicMode()
		else:
			folders = sys.argv[1:]
			for folder in folders:
				fileDic = {}
				fileDic = serachFile(folder,fileDic)
				name = os.path.basename(folder) + ".cbr"
				zipArchive(name,fileDic)
				print "Not compatible files: "
				for i in incompatible: print i

