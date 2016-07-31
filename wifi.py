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

def returnScanData(data):
    while True:
        data = subprocess.check_output("airport -s",shell=True) 
        if data: break
    return data

def doAction(device,opt,args):

    def switchControl(options): 
        return False if all(x for x in vars(opt).itervalues()) else True

    if switchControl(opt):
	if 'on' in args or 'off' in args:
            turn(args[0],device)
	if opt.optConnect:
            if exists(opt.optConnect):
                password = getpass.getpass("Enter %s password: " % opt.optConnect)
                connect(opt.optConnect,device,password)
                if is_connected(opt.optConnect):
                    print "Connection Success..."
            else:
                print "Network not found..."
        if opt.optLogout:
	    subprocess.call("sudo airport -z", shell=True)
	if opt.optScan:
		print "List of all wifi spots: "
                print returnScanData('')
    else:
        print "Error input..."

if __name__ == "__main__":
    (options,args) = getParser("Usage: %prog [option] on off")
    options_dict = vars(options)
    if args or any(x for x in options_dict.itervalues()): 
            doAction('en0',options,args)
    else:
        print "No input see the help"
