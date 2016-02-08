#!/usr/bin/env python

import os,sys
import zipfile
import optparse

images = ("jpg","jpeg","png","tiff","gif","bmp")
archives = ('cbr','cbz','cb7','zip')
incompatible = []

def testFile(file_,folder):
	return os.path.isfile(os.path.join(folder,file_)) and file_.split('.')[-1].lower() in images


#absolute path as a key ?  
def serachFile(directory,dictionary,globn):
	stream = os.listdir(directory)
	for input_ in stream:
		testDir = os.path.join(os.path.abspath(directory),input_)
		if os.path.isdir(testDir):
			 dictionary,globn = serachFile(testDir,dictionary,globn)
		else:
			if testFile(input_,directory):
				globn += 1
				hash_ = globn
				type_ = input_.split('.')[-1]
				pole = [input_,os.path.expandvars(os.path.realpath(directory)),type_]
				dictionary[hash_] = pole
			else:	
				if input_ not in incompatible: incompatible.append(input_)
	return (dictionary,globn) 

def printFile(what):
	sys.stdout.write(what)
	sys.stdout.flush()

def shorte(word):
	if len(word) > 7:
		word = "_" + word[-7:]
	return word

def zipArchive(name,dictionary,path_,mng):
	i = 1 
	f = zipfile.ZipFile(path_ + name + '.' + mng,'w')
	for dic in dictionary:
		printFile("\rAdding %s ( %s of %s) to %s" % (shorte(dictionary[dic][0]),'{0:0>3}'.format(i),len(dictionary),name))
		f.write('%s/%s' % (dictionary[dic][1],dictionary[dic][0]),'%s/%s%s.%s' % (name,name,'_{0:0>3}'.format(dic),dictionary[dic][2]))
		i += 1
	print ""
	f.close()

def testPath(path_):
	if path_ is None:
		path_ = '.'
	return str(path_) + '/'

def typeControl(type_):
	return 'cbr' if type_ is None or type_ not in archives else str(type_)
		
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

if len(sys.argv[1:]) > 0:
	if sys.argv[1] == "mode":
		comicMode()
	else:
		parser = optparse.OptionParser()
		parser.add_option('-d','--directory',dest='path',help='save to where')
		parser.add_option('-m','--manga',dest='mng',help='manga traders')
		
		(options,args) = parser.parse_args()
		if sys.argv[1] in ('-d','-h','-m'):
			folders = sys.argv[3:]
		else:
			folders = sys.argv[1:]
		for folder in folders:
			global_ = 0
			fileDic = {}
			fileDic,global_ = serachFile(folder,fileDic,global_)
			zipArchive(os.path.basename(folder),fileDic,testPath(options.path),typeControl(options.mng))
		if len(incompatible) > 0:
			print "Not compatible files: "
			for i in incompatible: print i
else:
	print "usage:  comic mode \n\tcomic -m zip file | comic -d path"

