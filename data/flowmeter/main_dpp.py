import json
import time
import datetime as dt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys

sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address


default_power_meter_data=json.loads('[{"address": 1, "power_meter_type": "DPP", "serial_number": "PM-TEST"}]')

def read_power_meter_registers(port, address, retries=3):
    retry_count = 0
    success = False
    register = None
    
    while not success and retry_count < retries:
        try:
            #read al 81 registers of the DFM at once
            register = port.read_holding_registers(0, 8, unit=address)
            print(register)
            if(len(register.registers)):
                success = True
            else: register=None
        except Exception as e:
            print(e)
        retry_count += 1
    return register
   
    
def read_all_power_meter(powermeters=default_power_meter_data):
    power_meter_data=[]
    power_meter_port = ModbusClient(method='rtu', port='/dev/DFM_SERIAL', timeout=1,baudrate=9600)
    print(power_meter_port)
    try:
        connection_status = power_meter_port.connect()
    except Err:
        print("Unable to connect PowerMeter\n".format(Err))
    
    if connection_status:
      #get the addresses from db
        print(powermeters)
        power_meter_data=[]
        for pm in powermeters:
            add = pm["address"]
            serial_number = pm["serial_number"]
            print('this is the address: {}'.format(add))
            register = read_power_meter_registers(power_meter_port, add)
            if not hasattr(register,'registers'):
                continue
            power_meter_data.append((register,add,serial_number))
    print('Power meter details are shown below:')
    print(power_meter_data)
    return power_meter_data
                
def main():
    read_all_power_meter()

if __name__ == '__main__':
    main()
        

