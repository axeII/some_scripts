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
    # use xml output to better print
    out = [d for d in data.replace('SECURITY (auth/unicast/group)','SECURITY').split(' ') if d != '']
    print ' '.join(out)

def doAction(device,opt,args):

    def switchControl(options): 
        return False if all(x for x in vars(opt).itervalues()) else True

    if switchControl(opt):
	if 'on' in args or 'off' in args:
            turn(args[0],device)
	if opt.optConnect:
		if exists(args[0]):
			password = getpass.getpass("Password: ")
			connect(args[0],device,password)
			if is_connected(args[0]):
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

if __name__ == "__main__":
    (options,args) = getParser("Usage: %prog [option] on off")
    options_dict = vars(options)
    if args or any(x for x in options_dict.itervalues()): 
            doAction('en0',options,args)
    else:
        print "No input see the help"
