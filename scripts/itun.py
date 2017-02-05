#!/usr/bin/env python

import optparse
import sys
import shutil
import os

def isMovie(movie):
    return os.path.isfile(movie) and movie.endswith('.mp4')

def aprove(file_,destination):
    return os.path.isfile(file_) and file_ not in destination

def create():
    return raw_input('Set path to move file: ') if raw_input('Do you want set path?[yes/no]: ') in ('yes','y') else '/Volumes/Macintosh SD/Movies/iTunes Movies/'

def move(what,where):
    if aprove(what,where):
        print "%s to %s \nMoving..." % (what,where)
        shutil.move(what,where)

def link(src,dst):
    #map(lambda x: x,(os.symlink(src,dst),print "Linking...")) if aprove(src,dst)
    if os.path.exists(os.path.abspath(src)):
        print "Linking..."
        os.symlink(src,dst)

def music(file_):
    if aprove(file_,"/Volumes/Macintosh SD/Music"):
        move(file_,"/Volumes/Macintosh SD/Music")
        link("/Volumes/Macintosh SD/Music/"+os.path.basename(file_),"/Users/ales/Music/" + os.path.basename(file_))

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-i','--itun',dest='itune',action='store_true',help='set itun')
    parser.add_option('-m','--musc',dest='music',action='store_true',help='set music')
    options,args = parser.parse_args()
    if args:
        if options.itune:
            for m_ in args:
                if isMovie(m_):
	            path = create()
		    move(os.path.abspath(movie),path+movie)
		    link(path+movie,os.path.abspath(movie))
		    print "I have successfuly itun " + movie
                else:
                    print "Not found supported movie: " + movie
        elif options.music:
            for m_ in args:
                music(os.path.abspath(m_))
	else:
            print "Error wrong input"
    else:
        print "no arguments"
