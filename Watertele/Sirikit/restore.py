import os

from time import sleep
from time import time
from datetime import datetime,timedelta

user_init_file = '/boot/water_init.cfg'
system_init_file = '/home/pi/water/waterparams.py'

if os.path.isfile(system_init_file)==True:
    print "Found " + system_init_file
    import waterparams as p

import waterfunctions as f

STA_CODE =  p.sta_code

print STA_CODE

try:
    tu_Config = f.GetTUConfig(STA_CODE+'1')
except:
    tu_Config = p.tu_Config

print (tu_Config)


STA_SI = tu_Config['Station_SI']

if len(STA_SI) < 2:
    STA_SI = '0' + STA_SI

WATER_DEVICE_ID = p.water_id +  STA_SI
RAIN_DEVICE_ID = p.rain_id + STA_SI

last_hour_date_time = datetime.now() - timedelta(days = 1)
print last_hour_date_time.strftime('%Y-%m-%d')
fname = last_hour_date_time.strftime('water_%Y-%m-%d.log')
print (fname)
fname2 = last_hour_date_time.strftime('rain_%Y-%m-%d.log')
print (fname2)

if os.path.isfile('/var/log/'+fname)==True:
    print ("read file")
    new_text = ''
    
    with open('/var/log/'+fname, 'r') as file_in:
        for line in file_in:
            print (line)
            ix = line.find('XX')
            if ix>0:
                l = line.split('|')
                print l
                xx_mark = 'XX'
                if f.reportUrlData(l[1],l[0],WATER_DEVICE_ID)==True:
                    xx_mark = 'OK'
                
                print (xx_mark)
                line = line[:ix] + xx_mark + '\n'
                
                sleep(5)
                        
            new_text = new_text + line 
            
    with open('/var/log/'+fname, 'w') as file_in:
        file_in.write(new_text)


if os.path.isfile('/var/log/'+fname2)==True:
    print ("read file")
    new_text = ''
    
    with open('/var/log/'+fname2, 'r') as file_in:
    
        for line in file_in:
            print (line)
            ix = line.find('XX')
            if ix>0:
                l = line.split('|')
                print l
                xx_mark = 'XX'
                if f.reportUrlData(l[1],l[0],RAIN_DEVICE_ID)==True:
                    xx_mark = 'OK'
                    
                print (xx_mark)
                line = line[:ix] + xx_mark + '\n'
                
                sleep(5)
            
            new_text = new_text + line

    with open('/var/log/'+fname2, 'w') as file_in:
        file_in.write(new_text)
        
        
        
#end_code
