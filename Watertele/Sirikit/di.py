import os
import RPi.GPIO as GPIO
import time
from datetime import datetime
from urllib2 import urlopen
from time import time
from time import sleep

import waterparams as p
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
dict = p.alarm_text
#alarm_text ={1:'Normal',0:'Alarm.'}
#dict = alarm_text

tu_Config = f.GetTUConfig(STA_CODE)	# f.getTUConfig(STA_CODE)

STA_SI = tu_Config['Station_SI']
if len(STA_SI) < 2:
	STA_SI = '0' + STA_SI

DEVICE_ID_DI0 = '12' + STA_SI
DEVICE_ID_DI1 = '13' + STA_SI
DEVICE_ID_DI2 = '14' + STA_SI
DEVICE_ID_DI3 = '15' + STA_SI
DEVICE_ID_DI4 = '16' + STA_SI

print STA_CODE
print STA_SI

TIMER_INTERVAL = 60*float(tu_Config['Interval'])

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
#print start_time

#di_pin1 = 15
di_pin2 = 18
di_pin3 = 22
di_pin4 = 29
di_pin5 = 33
#di_pin6 = 32
#di_pin7 = 37
#di_pin8 = 38

GPIO.setmode(GPIO.BOARD)
#GPIO.setup(di_pin1, GPIO.IN)
GPIO.setup(di_pin2, GPIO.IN)
GPIO.setup(di_pin3, GPIO.IN)
GPIO.setup(di_pin4, GPIO.IN)
GPIO.setup(di_pin5, GPIO.IN)
#GPIO.setup(di_pin6, GPIO.IN)
#GPIO.setup(di_pin7, GPIO.IN)
#GPIO.setup(di_pin8, GPIO.IN)


BB = 274877906945
AA = 0
di_o = [1,1,1,1,1,1,1,1]
di_n = [1,1,1,1,1,1,1,1]
di_o[0]= 0 #GPIO.input(di_pin1)
di_o[1]= int(GPIO.input(di_pin2))
di_o[2]= int(GPIO.input(di_pin3))
di_o[3]= int(GPIO.input(di_pin4))
di_o[4]= int(GPIO.input(di_pin5))
di_o[5]= 0 #GPIO.input(di_pin6)
di_o[6]= 0 #GPIO.input(di_pin7)
di_o[7]= 0
datetag=datetime.now().strftime('%Y-%m-%d')
timetag=datetime.now().strftime('%H:%M:%S')
dt = datetag + "%20" + timetag

#old[] = [di_n[0],di_n[1],di_n[2],di_n[3]]
f.reportUrlData(str(di_o[1]),dt,DEVICE_ID_DI0)
sleep(1)
f.reportUrlData(str(di_o[1]),dt,DEVICE_ID_DI1)
sleep(1)
f.reportUrlData(str(di_o[2]),dt,DEVICE_ID_DI2)
sleep(1)
f.reportUrlData(str(di_o[3]),dt,DEVICE_ID_DI3)
sleep(1)
f.reportUrlData(str(di_o[4]),dt,DEVICE_ID_DI4)
sleep(1)
#msg = "Station "+ StaCode + "-> DI2="+dict[di_o[1]] + "," + " DI3="+dict[di_o[2]] + "," + "DI4="+dict[di_o[3]] + "," + "DI5="+dict[di_o[4]] 
#f.line_notify(msg)

#start_time = time()
send_now = True

while True:
	di_n[0]= 0 #GPIO.input(di_pin1)
	di_n[1]= int(GPIO.input(di_pin2))
	di_n[2]= int(GPIO.input(di_pin3))
	di_n[3]= int(GPIO.input(di_pin4))
	di_n[4]= int(GPIO.input(di_pin5))
	di_n[5]= 0 #GPIO.input(di_pin6)
	di_n[6]= 0 #GPIO.input(di_pin7)
#	di_n[7]= GPIO.input(di_pin8)


 
	AA = (di_n[7]<<7 + di_n[6]<<6 + di_n[5]<<5 + di_n[4] << 4 + di_n[3]<<3 + di_n[2]<<2 + di_n[1]<<1 + di_n[0])
	if AA != BB:
		print AA
		BB = AA

#	print "%d%d%d%d% d%d%d%d" % (di_n[0], di_n[1], di_n[2], di_n[3], di_n[4], di_n[5], di_n[6], di_n[7])	
	print ("DI2 DI3 DI4 DI5")
	print  " %d   %d   %d   %d\n" % (di_n[1], di_n[2], di_n[3], di_n[4])	

	datetag=datetime.now().strftime('%Y-%m-%d')
	timetag=datetime.now().strftime('%H:%M:%S')
	dt = datetag + "%20" + timetag

        if di_n[1] != di_o[1]:
                print "di_n[1]=" + str(di_n[1])
		f.reportUrlData(str(di_n[1]),dt,DEVICE_ID_DI1)
		sleep(2)
		f.reportUrlData(str(di_n[1]),dt,DEVICE_ID_DI0)
		send_now = True
                di_o[1] = di_n[1]

        if di_n[2] != di_o[2]:
                print "di_n[2]=" + str(di_n[2])
		send_now = True
		f.reportUrlData(str(di_n[2]),dt,DEVICE_ID_DI2)
                di_o[2] = di_n[2]

        if di_n[3] != di_o[3]:
                print "di_n[3]=" + str(di_n[3])
		send_now = True
		f.reportUrlData(str(di_n[3]),dt,DEVICE_ID_DI3)
                di_o[3] = di_n[3]

        if di_n[4] != di_o[4]:
                print "di_n[4]=" + str(di_n[4])
		send_now = True
		f.reportUrlData(str(di_n[4]),dt,DEVICE_ID_DI4)
                di_o[4] = di_n[4]


	if send_now:
#		msg = "Station "+ STA_CODE + "-> DI2="+str(di_o[1])+"("+dict[di_n[1]] + "),"+" DI3="+str(di_o[2])+"("+dict[di_n[2]]+")," + "DI4="+str(di_o[3])+"("+dict[di_n[3]]+")," + "DI5="+str(di_o[4])+"("+dict[di_n[4]]+")" 
		msg = "Station "+ STA_CODE + "-> DI2="+dict[di_n[1]] + ", DI3="+dict[di_n[2]]+",DI4="+dict[di_n[3]]+",DI5="+dict[di_n[4]] 
		f.line_notify(msg)
		send_now = False

	end_time=time()
	if end_time-start_time>TIMER_INTERVAL:
		start_time = time()
		f.reportUrlData(str(di_n[1]),dt,DEVICE_ID_DI1)
		sleep(2)
		f.reportUrlData(str(di_n[2]),dt,DEVICE_ID_DI2)
		sleep(2)
		f.reportUrlData(str(di_n[3]),dt,DEVICE_ID_DI3)
		sleep(2)
		f.reportUrlData(str(di_n[4]),dt,DEVICE_ID_DI4)
		sleep(2)
		f.reportUrlData(str(di_n[1]),dt,DEVICE_ID_DI0)

		di_o[1] = di_n[1]
		di_o[2] = di_n[2]
		di_o[3] = di_n[3]
		di_o[4] = di_n[4]
#	time.sleep(.150)
	sleep(1)

#end_code
