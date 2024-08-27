#!/usr/bin/env python

import RPi.GPIO as GPIO
import datetime
import sys
import signal
import time
from datetime import datetime

#verbose = True		# global variable

############################################################################################################
############################################################################################################

import waterparams as p


def printusage(progname):
        print progname + ' <gpio-pin-number> <filename> [debug]'
        print 'Example usage: ' 
	print progname + ' 23 /path/to/mylogfile'
        print progname + ' 23 /path/to/mylogfile debug'
	sys.exit(-1)

def signal_handler(signal, frame):
        if verbose:
		print('You pressed Ctrl+C, so exiting')
	GPIO.cleanup()
        sys.exit(0)


def readvalue(myworkfile):
	try:
		f = open(myworkfile, 'ab+')		# open for reading. If it does not exist, create it
		value = int(f.readline().rstrip())	# read the first line; it should be an integer value
	except:
		value = 0				# if something went wrong, reset to 0
	#print "old value is", value
	f.close()	# close for reading
	return value

def readvalue15(myworkfile):
	try:
		f = open(myworkfile, 'ab+')		# open for reading. If it does not exist, create it
		value = int(f.readline().rstrip())	# read the first line; it should be an integer value
	except:
		value = 0				# if something went wrong, reset to 0
	#print "old value is", value
	f.close()	# close for reading
	return value


def writevalue(myworkfile,value):
	print myworkfile
	print value
	f = open(myworkfile, 'w')
	f.write((str(value)+ '\n'))			# the value
	f.write((str(datetime.now())+ '\n'))	# timestamp
	f.close()

def saveDaylog():
	fname =  datetime.now().strftime("/var/log/rainT_%Y-%m-%d.log")
	f = open(fname, 'a')
	f.write((str(datetime.now())+ '\n'))	# timestamp
	f.close()


def rain():
	try:
		f = open("/boot/rain.cfg", 'ab+')		# open for reading. If it does not exist, create it
		str = f.readline().rstrip()	# read the first line; it should be an integer value
		list = str.split (",")
	except:
		list = [0,0,0]				# if something went wrong, reset to 0
	#print "old value is", value
	f.close()	# close for reading
	return list[0]

############################################################################################################
############################################################################################################

######### Initialization


#### get input parameters:

#try:
#	mygpiopin = int(sys.argv[1])
#	logfile = sys.argv[2]
#except:
#	printusage(sys.argv[0])

verbose = True
#try:
#	if sys.argv[3] == 'debug':
#		verbose = True
#		print "Verbose is On"
#	else:
#		printusage(sys.argv[0])
#except:
#	pass


#list = rain()
mygpiopin = int(p.rain_pin)
logfile = "/var/log/acc-rain-counter.log"
logfile2 = "/var/log/prev15-rain-counter.log"
#printusage(mygpiopin)

#### if verbose, print some info to stdout

if verbose:
	print "GPIO is " + str(mygpiopin)
	print "Logfile1 is " + logfile
	print "Logfile2 is " + logfile2
	print "Current accumulator value is " + str(readvalue(logfile))
	print "Previous 15 minute value is " + str(readvalue15(logfile2))

#### setup

GPIO.setmode(GPIO.BOARD)
GPIO.setup(mygpiopin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

signal.signal(signal.SIGINT, signal_handler)	# SIGINT = interrupt by CTRL-C

time.sleep(1)

########## Main Loop 
print (datetime.now())
start_time = time.time()
while 1:
        end_time = time.time()
        if end_time-start_time > 300:
                print (datetime.now())
                start_time = time.time()
        xx =  GPIO.input(mygpiopin)
#       print (xx)
        if xx == 0:
                print xx
                time.sleep(0.03)
                xx =  GPIO.input(mygpiopin)
                if xx == 0:
                        while xx==0:
                                xx =  GPIO.input(mygpiopin)
                        counter=readvalue(logfile) + 1
                        counter2=readvalue15(logfile2) + 1
                        saveDaylog()
                        if verbose:
                                print "New value is", counter
                                print "New value in 15 minute is", counter2


                        writevalue(logfile,counter)
                        writevalue(logfile2,counter2)
        time.sleep(0.005)
#exit()

while 0:
	# wait for pin going up
	GPIO.wait_for_edge(mygpiopin, GPIO.FALLING)

	xx =  GPIO.input(mygpiopin)
	time.sleep(0.05)
#	while xx == 0:
#		xx =  GPIO.input(mygpiopin)
#		time.sleep(0.1)
	
	# read value from file
	print xx
	xx =  GPIO.input(mygpiopin)
	print xx
	if xx == 0:
		print "continue"
		continue


	GPIO.wait_for_edge(mygpiopin, GPIO.FALLING)

	# read value from file
	counter=readvalue(logfile) + 1
	counter2=readvalue15(logfile2) + 1
	if verbose:
		print "New value is", counter
		print "New value in 15 minute is", counter2


#	update_things(counter)
	# write value to file
	writevalue(logfile,counter)
	writevalue(logfile2,counter2)

	# and wait for pin going down

############################################################################################################
############################################################################################################



#end_code
