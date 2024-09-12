from datetime import datetime,timedelta
import os



last_hour_date_time = datetime.now() - timedelta(days = 3)
print last_hour_date_time.strftime('%Y-%m-%d')


fname = last_hour_date_time.strftime('%Y-%m-%d.log')

print fname

os.system('sudo rm /var/log/rain_' + fname)

fname = last_hour_date_time.strftime('%Y-%m-%d.log')

print fname

os.system('sudo rm /var/log/rainT_' + fname)

fname = last_hour_date_time.strftime('%Y-%m-%d.log')

print fname

os.system('sudo rm /var/log/water_' + fname)

