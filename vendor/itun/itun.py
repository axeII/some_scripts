#!/usr/local/bin/python
import sys
import shutil
import os

def isEmpty(args):
	if not args:
		return True

def isMovie(movie):
	state = False
	if os.path.isfile(movie) and movie.endswith("mp4"):
		state = True
	return state

def aprove(file_,destination):
	if os.path.isfile(file_):
		return True
	else:
		return False

def create():
	path = "/Volumes/Macintosh SD/Movies/iTunes Movies/"
	choice = raw_input('Do you want set path?[yes/no]: ')
	if choice == "yes" or choice == "y" or choice == "Y":
		path = raw_input('Set path to move file: ')
	return path			

def move(what,where):
	if aprove(what,where):		
		print "%s to %s \nMoving..." % (what,where)
		shutil.move(what,where)

def link(src,dst):
	if aprove(src,dst):	
		print "Linking..."
		os.symlink(src,dst)

if __name__ == "__main__":
	movies = sys.argv[1:]
	if not isEmpty(movies):
		for movie in movies:
			if isMovie(movie):
				path = create()
				move(os.path.abspath(movie),path+movie)
				link(path+movie,os.path.abspath(movie))
				print "I have successfuly itun " + movie		
			else:
				print "Not found " + movie
	else:
		print "Usage:\t itun movie.mp4 | movieTwo.mp4"



