#!/usr/bin/env python

import os,sys 
import subprocess
import getpass
import optparse

def getParser():
    parser = optparse.OptionParser()
    #parser.add_option()
    return parser.parse_args()

def is_connected(keyword):
	data = subprocess.check_output("airport -I")
	return keyword in data

def exists(keyword):
	data = subprocess.check_output("airport -s")
	return keyword in data	

def connect(name,device,password):
	if password:
		command = "networksetup -setairportnetwork %s %s %s" % (device,name,password)
		print "Connecting to %s network..." % name
                subprocess.call(command,shell=True)

def turn(action,device):
	command = "networksetup -setairportpower %s %s" % (device,action)
	print "Turning wifi " + str(action)
        subprocess.call(command,shell=True)

def doAction(device,args):
    if args and len(args) < 4:
	if 'on' in args or 'off' in args:
            turn(args[0],device)
	elif 'log' in args:
		if exists(args[1]):
			password = getpass.getpass("Password: ")	
			connect(args[1],device,password)
			if is_connected(network):
				print "Connection Success..."
		else:
			print "Network not found..."	
	elif 'logout' in args:
	    subprocess.call("sudo airport -z", shell=True)
	elif 'scan' in args:
		print "\t List of all wifi spots: "
		output = subprocess.check_output("airport -s",shell=True) 
                print output
    else:
        print "Error input..."
		
if __name__ == "__main__":
        (option,args) = getParser()
	if args:
                if len(args) > 3:
                    print "Ups too many arguments"
                doAction('en0',args)
	else:
		print "$ wifi - on | off | log | logout | scan"

