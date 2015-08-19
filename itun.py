#!/usr/local/bin/python

import shutil
import sys

# default paths ...
movieDir = "~/Music/iTunes/iTunes\ Media/Movies/"
myDir = "/Volumes/Macintosh\ SD/Movies/iTunes\ Movies/"

# procedure mv fileA to directory as fileB
def mv(fileA,fileB):
 if os.path.exits(fileA):
   shutil.move(fileA,fileB)
 else:
   print "File not found!"
   sys.exit(0)

def checkFile(fil):
  if fil.endswith(".mp4"):
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

 if soubor.endswith(".mp4"):
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
