#!/usr/bin/env python

import os,sys
import zipfile
import optparse

images = ("jpg","jpeg","png","tiff","gif","bmp")
archives = ('cbr','cbz','cb7','zip')
incompatible = []

def testFile(file_,folder):
	return os.path.isfile(os.path.join(folder,file_)) and file_.split('.')[-1].lower() in images

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

def clearName(name,control):
	return name.replace(" ",'_') if control else name

def resultName(defaultOne,optional):
    return optional if optional else defaultOne

def zipArchive(name,dictionary,path_,isZipfile):
	i = 1 
	if dictionary: 
		f = zipfile.ZipFile(path_ + clearName(name,isZipfile) + '.' + typeControl(isZipfile),'w')
		for dic in dictionary:
			printFile("\rAdding %8s ( %s of %s) to %s" % (shorte(dictionary[dic][0]),'{0:0>3}'.format(i),len(dictionary),name))
			f.write('%s/%s' % (dictionary[dic][1],dictionary[dic][0]),'%s/%s%s.%s' % (name,name,'_{0:0>3}'.format(dic),dictionary[dic][2]))
			i += 1
		print ""
		f.close()

def testPath(path_):
    return './' if not path_ else str(path_) + '/'

def extract(files,sourcePath,destionPath):
	for file_ in files:
		if file_[-3:] == 'cbr':
			zip_ref = zipfile.ZipFile(sourcePath + file_, 'r')
			zip_ref.extractall(destionPath)
			zip_ref.close()

def typeControl(status):
	return 'zip' if status else 'cbr'
		
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
                        print "Goodbye..."
		elif order == "R" or order == "r":
			print "Reseting from %s to 0" % (volume)
			volume = 0
		else:
			print "Wrong input.."

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-d','--dir',dest='path',help='save to where')
	parser.add_option('-z',dest='isZip',help='zipit',action='store_true',default=False)
	parser.add_option('-m',dest='mode',help='start the mode',action='store_true',default=False)
        parser.add_option('-n','--name',dest='name',help='set file name')
	(options,args) = parser.parse_args()
	if options.mode: comicMode()
	if args:
		for folder in args:
			global_ = 0
			fileDic = {}
			fileDic,global_ = serachFile(folder,fileDic,global_)
                        if options.isZip:
                            zipArchive(resultName(os.path.basename(folder),options.name),fileDic,testPath(options.path),True)
			zipArchive(resultName(os.path.basename(folder),options.name),fileDic,testPath(options.path),False)
		if len(incompatible) > 0:
			print "Not compatible files: "
			for i in incompatible: print i
	else:
		print "usage:  comic mode \n\tcomic -m zip file | comic -d path"
