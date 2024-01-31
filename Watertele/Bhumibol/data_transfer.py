import os
import json
import requests
from time import sleep
from time import time
from datetime import datetime
import waterparams
import waterfunctions

# user_init_file = '/boot/water_init.cfg'
# system_init_file = '/home/pi/water/waterparams.py'

# while os.path.isfile(user_init_file)==False:
#         print("waiting " + user_init_file)
#         sleep(2)

# cmd = 'sudo cp ' + user_init_file + ' ' + system_init_file
# print(cmd)
# os.system(cmd)



#USER_ID = waterparams.user_id

# log #########################################
import logging

log = os.getcwd() + "/log/log_DataTransfer.log"
logging.basicConfig(filename=log,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def WriteEventLog(strEvent):
    logging.info(" " + strEvent)
    print("" + strEvent)
################################################

def ReadValue(filename):
    try:
        with open(os.getcwd() + "/log/" + filename, "r") as file:
            value = file.readline().rstrip()
        return value

    except Exception as e:
        #value = 0                                   # if something went wrong
        WriteEventLog(str(e))

def WriteValue(filename, value):
    try:
        with open(os.getcwd() + "/log/" + filename, "w") as file:
            file.write(str(value))
    except Exception as e:
        WriteEventLog(str(e))
        sleep(1)

def AppendValue(filename, value):
    try:
        with open(os.getcwd() + "/log/" + filename, "a") as file:
            file.write(str(value))
    except Exception as e:
        WriteEventLog(str(e))
        sleep(1)

def TransferWater(mode):
    global prevWaterValue
    global waterValue
    try:
        xx_mark = 'XX'
        waterValue = float(ReadValue(logWater))

        if(mode == "True"):
            if(waterValue != prevWaterValue):
                msg = "Station : " + STA_CODE + " | " + dt_string + " | Maintenance Mode : " + mode + " | Water = " + str(waterValue)
                waterfunctions.LineNotify(msg)
                prevWaterValue = waterValue

        elif(mode == "False"):
            for i in range(5):
                if(waterfunctions.ReportUrlData(str(waterValue), dt_string, WATER_DEVICE_ID)==True):
                    xx_mark = 'OK'
                    print (xx_mark)
                    break
                sleep(20)
            info = dt_string + '|' + str(waterValue) + '|' + xx_mark + '\n'
            AppendValue(daylogWater, info)
    except Exception as e:
        WriteEventLog(str(e))

def TransferRain(mode):
    global rainCount
    global prevRainCount
    global rainValue
    try:
        xx_mark = 'XX'
        rainCount = int(ReadValue(logRainCount))                #current count
        if(os.path.exists(os.getcwd() + "/log/" + logPrevRainCount) == False):      #for the first times run
            WriteValue(logPrevRainCount, rainCount) 
        prevRainCount = int(ReadValue(logPrevRainCount))       #previous count
        rainValue = rainCount - prevRainCount               #calculate rain value
        if(rainValue < 0):
            rainValue = 0
        #WriteValue(logPrevRainCount, rainCount)            #current count -> previous count

        if((mode == "True") and (rainValue != 0)):
            msg = "Station : " + STA_CODE + " | " + dt_string + " | Maintenance Mode : " + mode + " | Rain = " + str(rainValue)
            waterfunctions.LineNotify(msg)

        elif(mode == "False"):
            for i in range(5):
                if(waterfunctions.ReportUrlData(str(rainValue), dt_string, RAIN_DEVICE_ID)==True):
                    xx_mark = 'OK'
                    print (xx_mark)                        
                    break
                sleep(20)
            info = dt_string + '|' + str(rainValue) + '|' + xx_mark + '\n'
            AppendValue(daylogRain, info)
    except Exception as e:
        WriteEventLog(str(e))
    finally:
        WriteValue(logPrevRainCount, rainCount)            #current count -> previous count

def TransferAmbient():
    try:
        ambientValue = json.loads(ReadValue(logAmbient))
        for i in range(len(ambientValue)):
            waterfunctions.ReportUrlData(str(ambientValue[i]/100), dt_string, AMBIENT_DEVICE_ID[i])
    except Exception as e:
        WriteEventLog(str(e))

def TransferAlarm(mode):
    try:
        alarmValue = json.loads(ReadValue(logAlarm))
        if(mode == "check"):
            changeFlag = 0
            for i in range(len(alarmValue)):
                if(alarmValue[i] != prevAlarmValue[i]):
                    changeFlag = 1
                    waterfunctions.ReportUrlData(str(int(not(alarmValue[i]))), dt_string, DI_DEVICE_ID[i])
                    prevAlarmValue[i] = alarmValue[i]

            if(changeFlag == 1):
                msg = "Station : " + STA_CODE + " -> DI0 = " + DICT_ALARM[alarmValue[0]] + " | DI1 = " + DICT_ALARM[alarmValue[1]] + " | DI2 = " + DICT_ALARM[alarmValue[2]] + " | DI3 = " + DICT_ALARM[alarmValue[3]] + " | DI4 = " + DICT_ALARM[alarmValue[4]]
                waterfunctions.LineNotify(msg)

        elif(mode == "normal"):
            for i in range(len(alarmValue)):
                waterfunctions.ReportUrlData(str(int(not(alarmValue[i]))), dt_string, DI_DEVICE_ID[i])
                prevAlarmValue[i] = alarmValue[i]
    except Exception as e:
        WriteEventLog(str(e))

def OnTheAirUpdate():
    try:
        for i in range(len(listUrlDownload)):
            while(1):
                response = requests.get(listUrlDownload[i], timeout=5)
                if(response.status_code == 200):
                    break
                else:
                    sleep(5)
            with open(os.getcwd() + '/' + listProgramName[i], 'wb') as file:
                file.write(response.content)

        WriteEventLog("Update Program Successfully")
        waterfunctions.UrlUpdateTUConfig(STA_CODE,'OntheAirUpdate','False')
        sleep(5)
        os.system("shutdown -t 0 -r -f")
    except Exception as e:
        WriteEventLog(str(e))

logRainCount = 'realtime_rain.log'
logPrevRainCount = 'prev_rain.log'
logWater = 'realtime_water.log'
logAlarm = 'realtime_alarm.log'
logAmbient = 'realtime_ambient.log'

urlWaterteleScan = 'https://raw.githubusercontent.com/lchokunl01/EGAT/main/Watertele/Bhumibol/watertele_scan.py'
urlDataTransfer = 'https://raw.githubusercontent.com/lchokunl01/EGAT/main/Watertele/Bhumibol/data_transfer.py'
urlRemoveLog = 'https://raw.githubusercontent.com/lchokunl01/EGAT/main/Watertele/Bhumibol/remove_log.py'
urlWaterfunctions = 'https://raw.githubusercontent.com/lchokunl01/EGAT/main/Watertele/Bhumibol/waterfunctions.py'
listUrlDownload = [urlWaterteleScan, urlDataTransfer, urlRemoveLog, urlWaterfunctions]
listProgramName = ['watertele_scan.py', 'data_transfer.py', 'remove_log.py', 'waterfunctions.py']

STA_CODE =	waterparams.sta_code

try:
    tu_Config = waterfunctions.GetTUConfig(STA_CODE)
except:
    tu_Config = waterparams.tu_Config

print (tu_Config)

STA_SI = tu_Config['Station_SI']
g_nInterval = int(tu_Config['Interval'])
g_strWaterType = tu_Config['Converter']
g_strRainGauge = tu_Config['RainGauge']
g_bMaintenance  = tu_Config['MaintenanceMode']
g_bReconfig = tu_Config['ReConfig']
g_bOntheAirUpdate = tu_Config['OntheAirUpdate']

if len(STA_SI) < 2:
    STA_SI = '0' + STA_SI

WATER_DEVICE_ID = waterparams.water_id + STA_SI
RAIN_DEVICE_ID = waterparams.rain_id + STA_SI
DI_DEVICE_ID = ["14" + STA_SI, "12" + STA_SI, "16" + STA_SI, "13" + STA_SI, "15" + STA_SI]
AMBIENT_DEVICE_ID = ["8" + STA_SI, "10" + STA_SI]

DICT_ALARM = waterparams.alarm_text

g_nLastTransferMinute = -1
g_nGetConfigConter = 0

waterValue = 0
prevWaterValue = 0
rainValue = 0
rainCount = 0
prevRainCount = 0
alarmValue = [0,0,0,0,0]
prevAlarmValue = [0,0,0,0,0]
ambientValue = [0,0]

WriteEventLog("Program Watertele BB : Data Transfer v1.7 20240131")

while(1):

    nowMinute = int(datetime.now().strftime("%M") )
    daylogWater = datetime.now().strftime("water_%Y-%m-%d.log")
    daylogRain = datetime.now().strftime("rain_%Y-%m-%d.log")
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")

    if(g_nGetConfigConter >= 3):        #15 sec
        g_nGetConfigConter = 0
        try:
            tu_Config = waterfunctions.GetTUConfig(STA_CODE)
            #if(tu_Config != ''):
            g_nInterval = int(tu_Config['Interval'])
            g_strWaterType = tu_Config['Converter']
            g_strRainGauge = tu_Config['RainGauge']
            g_bMaintenance  = tu_Config['MaintenanceMode']
            g_bReconfig = tu_Config['ReConfig']
            g_bOntheAirUpdate = tu_Config['OntheAirUpdate']
            print("Receive config")
            #else:
            #    print("Receive none")
        except Exception as e:
            WriteEventLog(str(e))

    g_nGetConfigConter += 1

    if(g_bOntheAirUpdate == 'True'):
        OnTheAirUpdate()

    if(g_bReconfig == 'True'):
        waterfunctions.UrlUpdateTUConfig(STA_CODE,'ReConfig','False')
        sleep(2)
        os.system("shutdown -t 0 -r -f")
        
    if(g_bMaintenance == 'True'):
        if (g_strWaterType != 'N/A'):
            TransferWater(g_bMaintenance)
        if (g_strRainGauge == 'True'):
            TransferRain(g_bMaintenance)
        TransferAlarm("check")

    else:

        if( (nowMinute%g_nInterval == 0) and (g_nLastTransferMinute != nowMinute) ):
        #if((g_nLastTransferMinute != nowMinute) ):
            print("Time to send")
            if (g_strWaterType != 'N/A'):
                TransferWater(g_bMaintenance)
                
            if (g_strRainGauge == 'True'):
                TransferRain(g_bMaintenance)

            TransferAmbient()
            TransferAlarm("normal")
            
            g_nLastTransferMinute = nowMinute
            

        #send immediatly when status changed
        TransferAlarm("check")
    
    sleep(5)

###end_code

#test