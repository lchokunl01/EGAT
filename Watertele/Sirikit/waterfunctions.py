import requests
import json

token = "YH20Lh14sUt01FEetHuJbN5yZ2lmJoJcGtwg5ZRVIfz"

def reportUrlData(f_data,dt,dataID):
        url = "https://watertele.egat.co.th/sirikit64/api/SentRawdata?User_ID=524522"
        url = url+"&TimeTag_DT=" + dt
        url = url+"&Device_ID=" + dataID
        url = url+"&RawData=" + f_data

        print (url)
        try:
                res = requests.post(url,timeout=30)
                print (res.text)
                new_dict = json.loads(res.text)
        except:
                return False

        if (new_dict["code"]) != '200':
                return False

        return True


def GetTUConfig(staID):
        url = "https://watertele.egat.co.th/sirikit64/api/GetTUConfig?StationCode=" + staID + "&User_ID=524522"
        print url
        try:
                r = requests.post(url,timeout=5)
        except:
                return None
        #print r.text
        t = r.text
        t=t.strip(']')
#       print t
        t=t.strip('[')
#       print t
        my_dict = json.loads(t)
        return my_dict

def GetMaintenanceMode(STA_CODE):
        try:
                my_dict = GetTUConfig(STA_CODE)
                print (my_dict)
                mntMode = my_dict["MaintenanceMode"]
        except:
                mntMode = 'xx'
        return  mntMode


def urlUpdateTUConfig(sta_code,target,valu):
        url= 'https://watertele.egat.co.th/sirikit64/api/SentTUConfig?User_ID=524522&Target='+target+'&Value='+valu+'&StationCode='+sta_code
        print (url)
        r = requests.post(url,timeout=30)
        print (r.text)

def line_notify(linemsg):
    try:
        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

        r = requests.post(url, headers=headers, data = {'message':linemsg})
        print (r.text)
    except:
        return


