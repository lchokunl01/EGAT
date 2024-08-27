import RPi.GPIO as GPIO
import time
from time import time
from time import sleep
import os
import subprocess
import glob
import sys
#import MySQLdb
#import urllib
from urllib2 import urlopen

from datetime import datetime

import waterfunctions as f


user_init_file = '/boot/water_init.cfg'
system_init_file = '/home/pi/water/waterparams.py'

while os.path.isfile(user_init_file)==False:
        print "waiting " +  user_init_file
        sleep(2)


if os.path.isfile(system_init_file)==True:
        print "Found " + system_init_file
        import waterparams as p

STA_CODE = p.sta_code

tu_Config = f.GetTUConfig(STA_CODE)     # f.getTUConfig(STA_CODE)

STA_SI = tu_Config['Station_SI']
if len(STA_SI) < 2:
        STA_SI = '0' + STA_SI


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#fanpin=33
FAN_PIN = 37
#GPIO.setup(fanpin, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

SERIAL = "XX"
REMOTE_URL = "XX"
CPUTEMP_KEY = "XX"
FAN_KEY = "XX"

TEMP_THRESHOLD = 60.0
TEMP_HYST = 10.0

m_list = []

fanDeviceID = p.fan_id + STA_SI
cpuDeviceID = p.cpu_id + STA_SI

print STA_CODE
print STA_SI


print "fanDeviceID = " + str(fanDeviceID)
print "cpuDeviceID = " + str(cpuDeviceID)
#print "Interval = " + str( Interval)

#Interval = 2
TIMER_INTERVAL = 60*int(tu_Config['Interval'])

print(datetime.now().strftime('%H:%M:%S'))
min = int(datetime.now().strftime('%M'))
ss = int(datetime.now().strftime('%S'))
current_sec = (min*60) + ss
interval_sec = current_sec % TIMER_INTERVAL
start_time  = time() - interval_sec
#print min
#print ss
#print current_sec
#print interval_sec

def get_threshold():
        #list from file conf.txt
        m_list.append(60.0)
        m_list.append(10.0)



def getCPUtemperature():
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))


def main():
        global SERIAL
        global REMOTE_URL
        global CPUTEMP_KEY
        global FAN_KEY

        get_threshold()
        print (m_list)
        TEMP_THRESHOLD = m_list[0]
        TEMP_HYST = m_list[1]
        print (TEMP_THRESHOLD)
        fan_stat_old = GPIO.input(FAN_PIN)
#        start_time = time() - (TIMER_INTERVAL - 1)
	print(datetime.now().strftime('%H:%M:%S'))
	min = int(datetime.now().strftime('%M'))
	ss = int(datetime.now().strftime('%S'))
	current_sec = (min*60) + ss
	interval_sec = current_sec % TIMER_INTERVAL
	start_time  = time() - interval_sec

        while 1:
                fan_stat_new = GPIO.input(FAN_PIN)
                if fan_stat_old != fan_stat_new:
                        fan_stat_old = GPIO.input(FAN_PIN)
	        	datetag=datetime.now().strftime('%Y-%m-%d')
        		timetag=datetime.now().strftime('%H:%M:%S')
			dt = datetag + "%20" + timetag
			f.reportUrlData(str(fan_stat_new),dt,fanDeviceID)
			f.reportUrlData(str(cputemperature),dt,cpuDeviceID)

#                print (fan_stat_new)
                sleep(5)
                cputemperature = getCPUtemperature()
#                print  (cputemperature)
                end_time = time()
                time_taken = end_time - start_time # time_taken is in seconds
#                print (time_taken)
                if time_taken >= TIMER_INTERVAL:
	        	datetag=datetime.now().strftime('%Y-%m-%d')
        		timetag=datetime.now().strftime('%H:%M:%S')
			dt = datetag + "%20" + timetag
			f.reportUrlData(str(cputemperature),dt,cpuDeviceID)
			f.reportUrlData(str(fan_stat_new),dt,fanDeviceID)
                        start_time = time()



   #control the fan based on the temp
                print (float(cputemperature) - TEMP_THRESHOLD)
                if float(cputemperature) > TEMP_THRESHOLD:
                        GPIO.output(FAN_PIN, True)
                        print ("fan on")
                if float(cputemperature) <= (TEMP_THRESHOLD - TEMP_HYST):
                        GPIO.output(FAN_PIN, False)
                        print ("fan off")

if __name__ == "__main__":
        main()


#end_code