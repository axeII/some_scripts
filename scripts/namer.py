#!/usr/bin/python

import optparse
import sys,os
import re,itertools
from random import randint
from os.path import *

def parseArgs():
    parser = optparse.OptionParser()
    parser.add_option('-r',dest='rex',help='Read number file by regex',action='store_true')
    parser.add_option('-p',dest='dirN',help='Rename all files by current directory',action='store_true')
    parser.add_option('-d',dest='sDir',help='Rename directory as well',action='store_true')
    parser.add_option('-f',dest='fileN',help='Exact name you want each file name')
    parser.add_option('-n',dest='noExe',help='Dry print just print all action not execute',action='store_true')
    parser.add_option('-c',dest='clean',help='acts like mv',action='store_true')
    parser.add_option('-e',dest='endn',help='end name',action='store_true')
    return parser.parse_args()

def filterArgs(args,options):
    field,paths = (list(),map(lambda x:dirname(realpath(x)),args))
    [field.append(os.listdir(a) if isdir(a) and not options.sDir else [a]) for a in args]
    return (list(itertools.chain.from_iterable(field)),(realpath(args[0])) if all(x==paths[0] for x in paths) else sys.exit('Some paths are diferent'),options)

def fixName(myPath,num,inp):
    return "%s/%s%s" % (myPath if isdir(myPath) else dirname(myPath),'{0:03d}'.format(num),splitext(inp)[1])

def nameThoseFiles(files,tPath,option):
    if option.dirN and option.fileN:
        sys.exit("Error too many switches")
    for i in range(len(files)):
        if files[i].startswith('.'):
            continue
        if option.dirN or option.fileN:
            if exists(join(dirname(tPath),option.fileN)):
                sys.exit('Ups wrong file name!')
            new ="%s/%s_%s%s" % (dirname(tPath),basename(tPath) if option.dirN else option.fileN,'{0:0>3}'.format(i),splitext(files[i])[1])
        elif option.rex:
            try:
                newIndex = int(re.findall(r'\d+',files[i])[-1])
            except IndexError:
                newIndex = 0
            new = fixName(tPath,newIndex,files[i])
        else:
            new = fixName(tPath,i,files[i])
        if option.noExe:
            print "renaming from %s to %s" % (files[i],basename(new))
        else:
            try:
                os.rename(join(dirname(tPath) if not isdir(tPath) else tPath,files[i]),new)
            except Exception as e:
                print 'Ups wrong naming: ',e

if __name__ == "__main__":
    (options,args) = parseArgs()
    #[nameThoseFiles([arg] if options.sDir else os.listdir(arg) if isdir(arg) else [arg],dirname(realpath(arg)),options) for arg in args] if args else sys.exit("No input")
    nameThoseFiles(*filterArgs(args,options)) if args else sys.exit('No inputs given...')
