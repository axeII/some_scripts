#!/usr/local/bin/python

import shutil
import sys
import optparse

# default paths ...
movieDir = "~/Music/iTunes/iTunes\ Media/Movies/"
myDir = "/Volumes/Macintosh\ SD/Movies/iTunes\ Movies/"
parser = optparse.OptionParser()
parser.addOption('-d','--destination',dest='destination', help='Place to save file')

#other options
(options,args) = parser.parser_args()

if options.destination is None:
    options.destination = myDir

sayWhat = 'file will be saved to ' + myDir

# function list
def mv(pathFile,pathTo):
    if os.path.exits(pathFile):
        shutil.move(pathFile,pathTo)
    else:
        print "File not found!"
        sys.exit(0)

def checkFile(_file):
    if _file.endswith(".mp4"):
	       return True
       else:
           return False

#this function maybe not needed
def checkDir(_dir):
    if (os.path.isdir(_dir)):
        return True
    else:
        return False

def ln(src,dst):
    if os.path.isdir(src) and os.path.isdir(dst):
        os.symlink(src,dst)
    else:
        print "Link is broken"
        sys.exit(0)

def findFile(arguments):
    fileName = ""
    for argu in arguments:
        if checkFile(argu):
            fileName = str(argu)
    return fileName

# main code

if len(sys.argv[1:]) >= 2 or len(sys.argv[1:]) >= 1:
     soubor = findFile(sys.argv[1:])
     if soubor != "" and checkDir(options.destination):
         mv(soubor,options.destination)
         ln(soubor,options.destination)
     else:
         print "File not found"
         sys.exit(0)
else:
  print "File not found or wrong dir "
  sys.exit(0)
