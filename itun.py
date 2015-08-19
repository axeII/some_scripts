#!/usr/local/bin/python

import shutil
import sys
import optparse

# default paths ...
movieDir = "~/Music/iTunes/iTunes\ Media/Movies/"
myDir = "/Volumes/Macintosh\ SD/Movies/iTunes\ Movies/"
parser = optparse.OptionParser()
parser.addOption('-d','--destination',dest='destination', help='Place to save file')

(options,args) = parser.parser_args()

if options.destination is None:
    options.destination = myDir

sayWhat = 'File, ',

# procedure mv fileA to directory as fileB
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

# procedure ln to create symbolic link
def ln(src,dst):
  if os.path.isdir(src) and os.path.isdir(dst):
      os.symlink(src,dst)
 else:
  print "Link is broken"
  sys.exit(0)

# main code

 if checkFile(sys.argv[2]):
     if len(sys.arg) > 1:
         destination = sys.arg[2]
         if (os.path.isdir(destination)):
            mv(soubor,destination)
         else:
             print "Directory dosnt exists"
             sys.exit(0)
     else:
         mv(soubor,destination)
else:
  print"File is not mp4 format"
  sys.exit(0)
