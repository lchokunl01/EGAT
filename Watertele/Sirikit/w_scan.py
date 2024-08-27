import serial
import minimalmodbus
import requests
import os
import random

# Generate a random number between 0 and 59
random_number = random.randint(0, 59)
print(random_number)


from time import sleep
from time import time
from datetime import datetime

import json

user_init_file = '/boot/water_init.cfg'
system_init_file = '/home/pi/water/waterparams.py'

while os.path.isfile(user_init_file)==False:
        print("waiting " +	user_init_file)
        sleep(2)

cmd = 'sudo cp ' + user_init_file + ' ' + system_init_file
print(cmd)
os.system(cmd)

if os.path.isfile(system_init_file)==True:
    print("Found " + system_init_file)
    import waterparams as p

import waterfunctions as f

#USER_ID = p.user_id
STA_CODE =	p.sta_code

print(STA_CODE)


# log #########################################
import logging

log = "log_wscan.log"
logging.basicConfig(filename=log,level=logging.ERROR,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def WriteEventLog(strEvent):
    logging.info(":" + strEvent)
    print(":" + strEvent)
################################################

def readvalue(myworkfile):
        try:
            f = open(myworkfile, 'ab+')				# open for reading. If $
            value = int(f.readline().rstrip())		# read the first line; $
            f.close()		# close for reading
        except:
            value = 0								# if something went wro$
        #print("old value is", value)
		
        return value

def readvalue15(myworkfile):
        try:
            f = open(myworkfile, 'ab+')				# open for reading. If $
            value = int(f.readline().rstrip())		# read the first line; $
            f.close()		# close for reading
        except:
            value = 0								# if something went wro$
        #print("old value is", value)
		
        return value

try:
    tu_Config = f.GetTUConfig(STA_CODE+'1')
    if(tu_Config == None):
        raise Exception('Cannot get config')
except:
    tu_Config = p.tu_Config

print(tu_Config)

logfile = "/var/log/acc-rain-counter.log"
logfile2 = "/var/log/prev15-rain-counter.log"
#printusage(mygpiopin)

#### if verbose, print some info to stdout

print("Logfile1 is " + logfile)
print("Logfile2 is " + logfile2)
print("Current accumulator value is " + str(readvalue(logfile)))
print("Previous 15 minute value is " + str(readvalue15(logfile2)))

sensor_interface_type = tu_Config['Converter']
interval = int(tu_Config['Interval'])

STA_SI = tu_Config['Station_SI']

if len(STA_SI) < 2:
    STA_SI = '0' + STA_SI

WATER_DEVICE_ID = p.water_id +	STA_SI
RAIN_DEVICE_ID = p.rain_id + STA_SI

now = datetime.now()
mn_o = int(now.strftime("%M"))

if sensor_interface_type == 'SDI12':
    ser = serial.Serial ("/dev/ttyAMA0", 1200, timeout=1)

elif sensor_interface_type == 'RS485Modbus':
    instrument = minimalmodbus.Instrument('/dev/ttyAMA0',1)
    instrument.serial.baudrate= 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_EVEN
    instrument.serial.stopbits = 1
else:
    sensor_interface_type = 'NONE'

next_mn = int(datetime.now().strftime("%M") )
start_time = time()
send_ok = 99
old_f_water = 9999
#os.system('sudo systemctl restart di.service')
#os.system('sudo systemctl restart fan.service')
pending_delete = False
counter2=0
old_counter=0
random_delay = random.randint(1, 59)       #random to delay send data

while 1:
    if sensor_interface_type == 'SDI12':
        try:
            s_water = ser.readline()
            if(s_water == ''):
                raise Exception("Can't read serial")
            sign =	s_water.find("+",0)
            if sign>0:
                f_water=float(s_water[sign:len(s_water)-1].strip())
            else:
                sign =	s_water.find("-",0)
                if sign>0:
                    f_water=float(s_water[sign:len(s_water)-1].strip())
                else:
                    continue
        except:
            f_water = 9999
        sleep(3)

    elif sensor_interface_type == 'RS485Modbus':
#       f_water = instrument.read_float(0x20,3,2,1)
        try:
            l = instrument.read_register(0x20,4,3,signed=True)
            f_water = float(l)	#(l[0]<<16)+l[1])/100000.00
        except:
            f_water = 9999
    elif sensor_interface_type == 'Adam':
        f_water = 0
    else:
        f_water = 0

    print(f_water)
    mn = int(datetime.now().strftime("%M") )
    fname =	 datetime.now().strftime("water_%Y-%m-%d.log")
    fname2 =  datetime.now().strftime("rain_%Y-%m-%d.log")
    d_string = datetime.now().strftime("%Y-%m-%d")
    t_string = datetime.now().strftime("%H:%M")
    dt_string = d_string + "%20" + t_string
    dt_string_x = d_string + " " + t_string
    end_time = time()
	
	
    if end_time-start_time>10:
        start_time = time()
        try:
            tu_Config = f.GetTUConfig(STA_CODE)
            if(tu_Config == None):
                raise Exception('Cannot get config')
        except:
            tu_Config = p.tu_Config
		
        print(tu_Config['MaintenanceMode'])
#       ota = tu_Config['OntheAirUpdate']
#       if ota=='True':
#           os.system('sudo python /home/pi/water/ota.py')
#           exit()
        recon = tu_Config['ReConfig']
        if recon == 'True':
		
            f.urlUpdateTUConfig(STA_CODE,'ReConfig','False')
            sleep(2)
            os.system('sudo reboot')
			
        RainGauge = tu_Config['RainGauge']
        interval  = int(tu_Config['Interval'])
        mnt_mode  = tu_Config['MaintenanceMode']
		
        print(interval)
        if mnt_mode == 'True':
            msg = "Station " + STA_CODE + " " + dt_string_x +" Maintenance Mode=" + mnt_mode + " " + sensor_interface_type + "=" + str(f_water)
            if old_f_water != f_water:
                f.line_notify(msg)
                old_f_water = f_water
				
            counter2=readvalue15(logfile2)
            print(counter2)
            print(old_counter)
			
            if counter2!=old_counter:
			
                if counter2>0:
                    msg = "Station " + STA_CODE + " " +dt_string_x +" RAIN=" + str(counter2)
                    f.line_notify(msg)
#               os.system('sudo rm '+logfile2)
                pending_delete = True
                old_counter = counter2
				

        else:
		
            old_f_water = 9999
            old_counter = 0
            if pending_delete==True:
			
                counter2=0
                os.system('sudo rm '+logfile2)
                pending_delete = False

        print(dt_string + " " + str(f_water))
#       if mn==next_mn:
        if mn%interval==0:
            print("Delay time (s): " + random_delay)
            sleep(random_delay)
		
            xx_mark = 'XX'
            print(send_ok)
            if mn==send_ok:
			
                print('continue')
                continue
                
            for i in range(5):
                try:
                    if f.reportUrlData(str(f_water),dt_string,WATER_DEVICE_ID)==True:
			
                        xx_mark = 'OK'
                        print(xx_mark)
#                       send_ok = mn
                        break
            
                except:
                    WriteEventLog("reportUrlData Error : Water")
                
                sleep(15)
                    
                
            if sensor_interface_type != 'NONE':
			
                if xx_mark == 'XX':
				
				
                    f1 = open('/var/log/'+fname,'a')
                    s_text = dt_string	+ '|' + str(f_water) + '|' + xx_mark
                    print(s_text)
                    f1.write(s_text + '\n')
                    f1.close()
					
					
            if RainGauge == 'True':
			
			
                xx_mark = 'XX'
                counter2=readvalue15(logfile2)
                
                
                for i in range(5):
                    try:
                        if f.reportUrlData(str(counter2),dt_string,RAIN_DEVICE_ID)==True:
				
                            xx_mark = 'OK'
                            print(xx_mark)
                            send_ok = mn
                    
                            if old_counter>0:
					
                                msg = "Station " + STA_CODE + " " + dt_string_x + " Maintenance Mode=" + mnt_mode + ", Rain counter reset to Zero "
                                f.line_notify(msg)
                                
                            break
                            
                    except:
                        WriteEventLog("reportUrlData Error : Rain")
                    
                    sleep(30)

#               if xx_mark == 'XX':
                f1 = open('/var/log/'+fname2,'a')
                s_text = dt_string	+ '|' + str(counter2) + '|' + xx_mark
                print(s_text)
                f1.write(s_text + '\n')
                f1.close()
				

                os.system('sudo rm '+logfile2)
				

                os.system('sudo systemctl restart rain-counter.service')
				

            send_ok = mn
			

    sleep(2)
###end_code
