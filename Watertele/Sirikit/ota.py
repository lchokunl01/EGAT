import os
from time import sleep
import requests

import waterfunctions as f


dict_service = {1:'waterscan.service',2:'sht15.service',3:'di.service',4:'rain-counter.service',5:'fan.service'}
dict_fname = {1:'w_scan.py',2:'shi15.py',3:'di.py',4:'rain-counter.py',5:'restore.py'}
dict_link = {1:'https://ecp.egat.co.th/index.php/s/OYgBleapeNG0w3m',
	     2:'https://ecp.egat.co.th/index.php/s/jGBn0ibp48RFk6L',
	     3:'https://ecp.egat.co.th/index.php/s/iUdos0EUgLdrBRS',
	     4:'https://ecp.egat.co.th/index.php/s/VRj2yyrzwEbwEGE',
	     5:'https://ecp.egat.co.th/index.php/s/rgA8hqWQGum9wUG'
	}

user_init_file = '/boot/water_init.cfg'
system_init_file = '/home/pi/water/waterparams.py'

while os.path.isfile(user_init_file)==False:
    print("waiting " +  user_init_file)
    sleep(2)

if os.path.isfile(system_init_file)==True:
	print("Found " + system_init_file)
	import waterparams as p

STA_CODE =  p.sta_code

tu_Config = f.GetTUConfig(STA_CODE)
ota = tu_Config['OntheAirUpdate']
if ota=='False':
    exit()

for i in dict_fname:
    print (dict_link[i])
    cmd = 'sudo wget ' + dict_link[i] + '/download -O /tmp/'  + dict_fname[i]
    print(cmd)
    os.system(cmd)

    file_not_exists = True

    while file_not_exists:
        print(file_not_exists)
        if os.path.isfile('/tmp/'+ dict_fname[i])==False:
            print("waiting " + '/tmp/'+dict_fname[i])
            sleep(2)
        else:
            file_not_exists = False

    print ("read file")

    with open('/tmp/'+dict_fname[i]) as file_in:
        for line in file_in:
#			print (line)
            ix = str(line).find('end_code',0)
            if ix > 0:
                os.system('sudo rm /home/pi/water/'+dict_fname[i])
                sleep(1)
                cmd = 'sudo cp /tmp/'+dict_fname[i] +' /home/pi/water/'+dict_fname[i]
                print (cmd)
                os.system(cmd)
                sleep(1)
				
for i in dict_service:
    os.system('sudo systemctl restart ' + dict_service[i])

sleep(5)
f.urlUpdateTUConfig(STA_CODE,'OntheAirUpdate','False')


