import requests
import json
import os

token = "NlhvA2B8k6ADSbJnAUZFAD54so6DhIyo4LkLN062i1t"
'''
# log #########################################
import logging

log = os.getcwd() + "/log/log_transfer_error.log"
logging.basicConfig(filename=log,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def WriteEventLog(strEvent):
    logging.info(":" + strEvent)
    print(":" + strEvent)
################################################
'''
def ReportUrlData(f_data,dt,dataID):
    url = "https://watertele.egat.co.th/Bhumibol65/api/SentRawdata?User_ID=597924"
    url = url + "&TimeTag_DT=" + dt
    url = url + "&Device_ID=" + dataID
    url = url + "&RawData=" + f_data

    print (url)
    try:
        res = requests.post(url=url,timeout=30)
        print (res.text)
        result = json.loads(res.text)
        if(result["code"] != '200'):
            return False
        else:
            return True

    except Exception as e:
        #WriteEventLog(str(e))
        print(str(e))
        return False

def GetTUConfig(staID):
    url = "https://watertele.egat.co.th/Bhumibol65/api/GetTUConfig?StationCode=" + staID + "&User_ID=597924"
    print (url)
    try:
        r = requests.post(url=url,timeout=5)
    except:
        return None
    #print r.text
    t = r.text
    t=t.strip(']')
#   print t
    t=t.strip('[')
#   print t
    my_dict = json.loads(t)
    return my_dict

def UrlUpdateTUConfig(sta_code,target,value):
    url= 'https://watertele.egat.co.th/Bhumibol65/api/SentTUConfig?User_ID=597924&Target='+target+'&Value='+value+'&StationCode='+sta_code
    print(url)
    try:
        r = requests.post(url=url,timeout=10)
        print(r.text)
    except Exception as e:
        print(str(e))
        #WriteEventLog(str(e))

def LineNotify(linemsg):
    try:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

        r = requests.post(url, headers=headers, data = {'message':linemsg})
        print (r.text)
    except:
        return



'''
def ReadValue(myworkfile):
    try:
        file = open(myworkfile, 'r')              # open for reading. If $
        value = int(file.readline().rstrip())          # read the first line; $
        file.close()                                # close for reading
    except Exception as e:
        value = 0                                   # if something went wro$
        WriteEventLog(str(e))
    #print "old value is", value

    return value

from datetime import datetime
mn = int(datetime.now().strftime("%M") )
fname = datetime.now().strftime("water_%Y-%m-%d.log")
fname2 = datetime.now().strftime("rain_%Y-%m-%d.log")
d_string = datetime.now().strftime("%Y-%m-%d")
t_string = datetime.now().strftime("%H:%M")
dt_string = d_string + "%20" + t_string
dt_string_x = d_string + " " + t_string
dt_test = datetime.now().strftime("%Y-%m-%d %H:%M")

#logfile_rain = os.getcwd() + "/realtime_rain.log"

#rainValue = ReadValue(logfile_rain)
                
#reportUrlData(str(rainValue),dt_test,"201")
#print(type(os.getcwd()))


reportUrlData('1', dt_string_x, "401")

'''