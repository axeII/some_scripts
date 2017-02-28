#!/usr/local/bin/python3

import os
import time
import optparse
from os.path import expanduser
from subprocess import call, STDOUT, CalledProcessError

hostnames = ("8.8.8.8","8.8.4.4","139.130.4.5")
runout = 0
timetoreset = 0

def parse_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-o',dest='output_on',help='Output to standart output',action='store_true')
    return parser.parse_args()

def runoutfn(default):
    return True if default > 8 else False

def check_print(options,str_):
    FILE = expanduser("~/Desktop/pinger.log")
    with open(os.path.abspath(FILE),'a') as file_:
        print(str_) if options.output_on else file_.write('\n'+str_)

try:
    options,args = parse_arguments()
    start = time.time()
    start2 = time.time()
    while True:
        try:
            for host in hostnames:
                response = call("ping -c 1 %s 1>/dev/null"%host,shell=True)
                if response == 0:
                    break
        except Exception:
            runout += 1
        if response != 0:
            call("rnet 1>/dev/null",shell=True)
            check_print(options,"Rebooted network at " + time.strftime("[%Y-%m-%d %H:%M]"))
            timetoreset += 1
            runout += 1
        # set to seconds
        if (divmod(time.time()-start2,3600*60)[1]) < 40 and runoutfn(runout):
            raise KeyboardInterrupt
        else:
            runout = 0
            start2 = time.time()

        time.sleep(5)
    check_print(options,'Script has ended %s,%s' % (runout,timetoreset))

except KeyboardInterrupt:
    check_print(options,"Have to reset network %s times" % timetoreset)
    hours, rem = divmod(time.time()-start, 3600)
    minutes, seconds = divmod(rem, 60)
    check_print(options,"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
    #print("--- This program last for %s seconds ---" % (time.time() - start_time))
