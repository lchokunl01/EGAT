from time import sleep
import minimalmodbus
import serial
import os
import waterparams
import waterfunctions

HOLDING_REGISTER = 3
INPUT_REGISTER = 4
STATUS_REGISTER = 2

insrtrument_water_address = 1
insrtrument_rain_address = 2
insrtrument_alarm_address = 3
insrtrument_ambient_address = 65

# log #########################################
import logging

log = os.getcwd() + "/log/log_WaterteleScan.log"
logging.basicConfig(filename=log,level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def WriteEventLog(strEvent):
    logging.info(" " + strEvent)
    print("" + strEvent)
################################################

def read_modbus_data(modbus_device_address,int_register_start,int_register_length,register_type):
    instrument = minimalmodbus.Instrument('COM3', modbus_device_address)  # port name, slave address (in decimal)
    #instrument.serial.port = 'COM4'                     # this is the serial port name
    instrument.serial.baudrate = 9600         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 0.5        # seconds
    #instrument.address = 1                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.close_port_after_each_call = True

    result = ''
    try:
        instrument.address = modbus_device_address                    # this is the slave address number
        if register_type>2:
            result = instrument.read_registers(int_register_start,int_register_length,register_type)
        else:
            result = instrument.read_bits(int_register_start,int_register_length,register_type)

        #print(result)   
    except Exception as e:
        instrument.serial.close()

    return result

def read_water_data(modbus_device_address,int_register_start,decimal_place,register_type,parity_type):
    instrument = minimalmodbus.Instrument('COM3', modbus_device_address)  # port name, slave address (in decimal)
    #instrument.serial.port = 'COM4'                     # this is the serial port name
    instrument.serial.baudrate = 9600         # Baud
    instrument.serial.bytesize = 8
    if(parity_type == 'NONE'):
        instrument.serial.parity   = serial.PARITY_NONE
    elif(parity_type == 'EVEN'):
        instrument.serial.parity   = serial.PARITY_EVEN
    instrument.serial.stopbits = 1
    instrument.serial.timeout  = 1        # seconds
    #instrument.address = 1                         # this is the slave address number
    instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    instrument.close_port_after_each_call = True

    result = ''
    try:
        instrument.address = modbus_device_address                    # this is the slave address number
        result  = instrument.read_register(int_register_start,decimal_place,register_type,signed=True)

        #print(result)   
    except Exception as e:
        instrument.serial.close()

    return result

def WriteValue(filename, value):
    try:
        with open(os.getcwd() + "/log/" + filename, "w") as file:
            file.write(value)
    except Exception as e:
        WriteEventLog(str(e))
        sleep(1)

STA_CODE =	waterparams.sta_code
try:
    tu_Config = waterfunctions.GetTUConfig(STA_CODE)
except:
    tu_Config = waterparams.tu_Config

waterValue = ''
rainCount = ''
alarmValue = ''
ambientValue = ''

WriteEventLog("Program Watertele BB : Watertele Scan v1.3 20231011")

while(1):
    try: 

        #water level
        if(tu_Config['Converter'] == 'SDI12'):
            waterValue = str(read_water_data(insrtrument_water_address,0,3,HOLDING_REGISTER,'NONE'))
        elif(tu_Config['Converter'] == 'RS485Modbus'):
            waterValue = str(read_water_data(insrtrument_water_address,32,3,HOLDING_REGISTER,'EVEN'))
        print (waterValue)
        if(waterValue != ''):
            WriteValue("realtime_water.log", waterValue)
            sleep(1)
        
        #rain counter
        if (tu_Config['RainGauge'] == 'True'):
            rainCount = read_modbus_data(insrtrument_rain_address,2,1,HOLDING_REGISTER)
        print (rainCount)
        if(rainCount != ''):
            WriteValue("realtime_rain.log", str(rainCount[0]))
            sleep(1)

        #alarm 8 values
        alarmValue = str(read_modbus_data(insrtrument_alarm_address,0,5,STATUS_REGISTER))
        print (alarmValue)   #[0:7]
        if(alarmValue != ''):
            WriteValue("realtime_alarm.log", alarmValue)
            sleep(1)
        
        #ambient 2 values
        ambientValue = str(read_modbus_data(insrtrument_ambient_address,0,2,INPUT_REGISTER))
        print (ambientValue)   #[0:1]
        if(ambientValue != ''):
            WriteValue("realtime_ambient.log", ambientValue)
            sleep(1)

    except Exception as e:
        WriteEventLog(str(e))
        sleep(5)

    
    
        
    
   


