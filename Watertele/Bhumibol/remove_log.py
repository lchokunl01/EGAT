from datetime import datetime,timedelta
from time import sleep
import os

while(1):

    purge_day = datetime.now() - timedelta(days = 3)

    fname = purge_day.strftime('%Y-%m-%d.log')
    print(fname)

    log_rain = os.getcwd() + "/log/rain_" + fname
    log_water = os.getcwd() + "/log/water_" + fname

    if os.path.exists(log_rain):
        print(log_rain)
        os.remove(log_rain)

    if os.path.exists(log_water):  
        print(log_water)
        os.remove(log_water)

    sleep(86400)        #1 day

#os.system('rm ' + os.getcwd() + "/log/*" + fname)



