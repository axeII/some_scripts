#!/usr/bin/env python

import os,sys,re
import subprocess
import getpass
import optparse

def getParser(usage):
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c','--connect',action='optConnect',help='Which wifi you want to connect')
    parser.add_option('-l','--logout',action='optLogout',help='logout from wifi network')
    parser.add_option('-s','--scan',action='optScan',help='scan local network area')
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
    out = [d for d in data.replace('SECURITY (auth/unicast/group)','SECURITY').split(' ') if d != '']
    print ' '.join(out)
        
def doAction(device,opt,args):
    if args and len(args) < 2:
	if 'on' in args or 'off' in args:
            turn(args[0],device)
	elif 'log' in args:
		if exists(args[1]):
			password = getpass.getpass("Password: ")
			connect(args[1],device,password)
			if is_connected(args[1]):
				print "Connection Success..."
		else:
			print "Network not found..."
	elif 'logout' in args:
	    subprocess.call("sudo airport -z", shell=True)
	elif 'scan' in args:
		print "\t List of all wifi spots: "
		betterPrint(subprocess.check_output("airport -s",shell=True)) #too long timing load before exec.
    else:
        print "Error input..."

if __name__ == "__main__":
        (option,args) = getParser("usage: %prog [option] on off")
	if args:
                if len(args) > 2:
                    print "Ups too many arguments"
                    sys.exit(21)
                doAction('en0',option,args)
	else:
            print "No input see the help"
