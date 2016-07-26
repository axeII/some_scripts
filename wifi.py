#!/usr/local/bin/python

import os
import sys
import getpass

def is_connected(keyword,tempfile):
	os.system("airport -I > " + tempfile)
	f = open(tempfile,'r')
	data = f.read()
	f.close()
	return keyword in data

def exists(keyword,tempfile):
	os.system("airport -s > " + tempfile)
	f = open(tempfile,'r')
	data = f.read()
	f.close()
	return keyword in data	

def connect(name,device,password):
	if password != "":
		command = "networksetup -setairportnetwork %s %s %s" % (device,name,password)
		print "Connecting to %s network..." % (name)
		os.system(command)


def turn(action,device):
	command = "networksetup -setairportpower %s %s" % (device,action)
	os.system(command)
	print "Turning wifi " + action

def doAction(input_,network):
	device = "en0"
	if input_ == "on" or input_ == "off":
		turn(input_,device)
	elif input_ == "log":
		if exists(network,"/Users/Ales/Library/WifiLog/airport-scan.txt"):
			password = getpass.getpass("Password: ")	
			connect(network,device,password)
			if is_connected(network,"/Users/Ales/Library/WifiLog/connectino-info.txt"):
				print "Connection Success..."
		else:
			print "Network not found..."	
	elif input_ == "logout":
		os.system("sudo airport -z")
	else:
		print "Error input..."
		
if __name__ == "__main__":

	if len(sys.argv) > 1:
		cliAct = sys.argv[1]
		if len(sys.argv) == 2:
			doAction(cliAct,"")
		elif len(sys.argv) == 3:
			net = sys.argv[2]
			doAction(cliAct,net)
		else:
			print "Ups too many arguments"
	else:
		print "wifi on | off | log"

