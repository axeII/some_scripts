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

def serachFile(directory,listX):
	files = os.listdir(directory)
	for dir_ in files:
		if os.path.isdir(dir_):
			serachFile(dir_,list_)
		else:
			for d in directory:
				print d 
				#newList = []
				#if testFile(d):
					#newList.append(d)	
				#else:
				#	print "File %s is not compatible..." % (dir_)
			list_.append(newList)

def printFile(fileX,nameX):
	print "Adding %s to %s " % (fileX,nameX)

def archive(image):
	return os.path.abspath(image)

def zipArchive(name,folder,list_):
	#f = zipfile.ZipFile("./" + name,'w')
	finalList = map(archive,list_)
	for fin in finalList:
		printFile(fin,name)
	#	f.write(fin)
	#f.close()

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

	
# Coping image (1 of 100) to filenam1.cbr 	
# Coping image (22 of 67) to filenam2.cbr

if __name__ == "__main__":
	if len(sys.argv[1:]) < 1:
		print "navod"
	else:
		if sys.argv[1] == "mode":
			comicMode()
		else:
			folders = sys.argv[1:]
			for folder in folders:
				list_ = []
				serachFile(folder,list_)
				name = os.path.basename(folder) + ".cbr"
				print name, folder,list_
				#zipArchive(name,folder,list_)

