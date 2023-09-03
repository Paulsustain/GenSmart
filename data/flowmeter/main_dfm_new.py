import json
import time
import datetime as dt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys

sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
from smartgen.DFM_enumerators import DFM_status
import smartgen.flowmeter_data_converter as flowmeter_data_converter 

default_flowmeter_data=json.loads('[{"address": 111, "meter_type": "DFM", "serial_number": "FM-TEST"}]')

def read_dfm_registers(port, address, retries=3):
    retry_count = 0
    success = False
    register = None
    
    while not success and retry_count < retries:
        try:
            #read al 81 registers of the DFM at once
            register = port.read_holding_registers(0, 81, unit=address)
            print(register)
            if(len(register.registers)):
                success = True
            else: register=None
        except Exception as e:
            print(e)
        retry_count += 1
    return register
   
    
def read_all_dfm(flowmeters=default_flowmeter_data):
    flowmeter_data=[]
    dfm_port = ModbusClient(method='rtu', port='/dev/DFM_SERIAL', timeout=1,baudrate=9600)
    print(dfm_port)
    try:
        connection_status = dfm_port.connect()
    except Err:
        print("Unable to connect DFM\n".format(Err))
    
    if connection_status:
      #get the addresses from db
        print(flowmeters)
        for fm in flowmeters:
            add = fm["address"]
            serial_number = fm["serial_number"]
            print('this is the address: {}'.format(add))
            register = read_dfm_registers(dfm_port, add)
            if not register:
                continue
            flowmeter_data.append((register,add,serial_number))
    print('Flowmeter details are shown below:')
    print(flowmeter_data)
    return flowmeter_data
                
def main():
    read_all_dfm()

if __name__ == '__main__':
    main()
        

