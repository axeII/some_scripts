#!/usr/bin/env python

import os,sys,re
import subprocess
import getpass
import optparse

def getParser(usage):
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c','--connect',dest='optConnect',help='Which wifi you want to connect')
    parser.add_option('-l','--logout',dest='optLogout',help='logout from wifi network',action='store_true')
    parser.add_option('-s','--scan',dest='optScan',help='scan local network area',action='store_true')
    return parser.parse_args()

def is_connected(keyword):
    return keyword in subprocess.check_output("airport -I",shell=True)

def exists(keyword):
    return keyword in subprocess.check_output("airport -s",shell=True)

def connect(name,device,password):
    if password:
	command = "networksetup -setairportnetwork %s %s %s" % (device,name,password)
	print "Connecting to %s network..." % name
        subprocess.call(command,shell=True)

def turn(action,device):
    command = "networksetup -setairportpower %s %s" % (device,action)
    print "Turning wifi " + str(action)
    subprocess.call(command,shell=True)

def betterPrint(data):

    def deSerialize(arrRepresentation):
        arrRepresentation = arrRepresentation[1:len(arrRepresentation) - 2]
        return [x.replace("\'", "") for x in arrRepresentation.split(',')]

    def arrayDict(arr):
        data = {}
        header = []

        for el in arr:
            data[el] = []
            header.append(el)
            if el.find("\n") != -1:
                break

        for i in range(len(header), len(header)):
            for j in range(len(header)):
                data[header[j]] = arr[i + j]

        return data


    out = [d for d in data.replace('SECURITY (auth/unicast/group)','SECURITY').split(' ') if d != '']
    print ' '.join(out)
    #print arrayDict(deSerialize(data))

def doAction(device,opt,args):
    def switchControl(options): 
        return False if options.optScan and options.optConnect and options.optLogout else True 

    if switchControl(opt):
	if 'on' in args or 'off' in args:
            turn(args[0],device)
	if opt.optConnect:
		if exists(args[1]):
			password = getpass.getpass("Password: ")
			connect(args[1],device,password)
			if is_connected(args[1]):
				print "Connection Success..."
		else:
			print "Network not found..."
        if opt.optLogout:
	    subprocess.call("sudo airport -z", shell=True)
	if opt.optScan:
		print "\t List of all wifi spots: "
		betterPrint(subprocess.check_output("airport -s",shell=True)) #too long timing load before exec.
    else:
        print "Error input..."
        sys.exit(32)

if __name__ == "__main__":
        (options,args) = getParser("usage: %prog [option] on off")
        sys.exit
	if args or options.optScan or options.optLogout or options.optConnect:
                doAction('en0',options,args)
	else:
            print "No input see the help"
