import os
import RPi.GPIO as GPIO
import time
from datetime import datetime
from time import time
from time import sleep
from sht_sensor import Sht

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

tu_Config = f.GetTUConfig(STA_CODE)	# f.getTUConfig(STA_CODE)

STA_SI = tu_Config['Station_SI']
if len(STA_SI) < 2:
	STA_SI = '0' + STA_SI

temp_id  = p.temp_id + STA_SI
humid_id = p.humid_id + STA_SI

print STA_CODE
print STA_SI

TIMER_INTERVAL = 60*float(tu_Config['Interval'])

print(datetime.now().strftime('%H:%M:%S'))
min = int(datetime.now().strftime('%M'))
ss = int(datetime.now().strftime('%S'))
current_sec = (min*60) + ss
interval_sec = current_sec % TIMER_INTERVAL
start_time  = time() - interval_sec

#di_pin1 = 15
data_pin1 = 18
sck_pin = 7


#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(di_pin1, GPIO.IN)
datetag=datetime.now().strftime('%Y-%m-%d')
timetag=datetime.now().strftime('%H:%M:%S')
dt = datetag + "%20" + timetag


#start_time = time()
send_now = True

while True:
	try:
		sht = Sht(sck_pin, data_pin,voltage=ShtVDDLevel.vdd_5v)
		Temperature = sht.read_t()
		Humidity =  sht.read_rh()
#		print 'Temperature', sht.read_t()
#		print 'Relative Humidity', sht.read_rh()
	except:
		Temperature = 9999
		Humidity = 9999


	print 'Temperature', Temperature
	print 'Relative Humidity', Humidity
	datetag=datetime.now().strftime('%Y-%m-%d')
	timetag=datetime.now().strftime('%H:%M:%S')
	dt = datetag + "%20" + timetag


	end_time=time()
	if end_time-start_time>TIMER_INTERVAL:
		start_time = time()
		f.reportUrlData(str(Temperature),dt,temp_id)
		f.reportUrlData(str(Humidity),dt,humid_id)

#	time.sleep(.150)
	sleep(2)

#end_code