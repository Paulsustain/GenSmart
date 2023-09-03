import json
import time
import datetime as dt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys
import serial
from serial import Serial
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
sys.path.append('/home/pi/smarteye/helpers/smartgen')
from helper import get_device_mac_address as get_mac_address
import dpm_data_parser

port=Serial(port='/dev/DFM_SERIAL',baudrate=9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)
default_power_meter_data=json.loads('[{"address": 1, "power_meter_type": "DPM", "serial_number": "PM-TEST"}]')
retries=3
def read_energy_meter_registers(address=1,equipment_id=1):
    retry_count = 0
    success = False
    register = None
    
    while not success and retry_count < retries:
        try:
            
            power_dict={}
            power_dict.update(dpm_data_parser.get_phase_voltage(port,address))
            power_dict.update(dpm_data_parser.get_phase_current(port,address))
            power_dict.update(dpm_data_parser.get_line_voltage(port,address))
            power_dict.update(dpm_data_parser.get_power_factor(port,address))
            power_dict.update(dpm_data_parser.get_frequency(port,address))
            power_dict.update(dpm_data_parser.get_active_power(port,address))
            power_dict.update(dpm_data_parser.get_energy_data(port,address))
            address_dict={'address':address,'equipment':equipment_id}
            power_dict.update(address_dict)
            print(power_dict)
            if(bool(power_dict)):
                success = True
            else: power_dict={}
        except Exception as e:
            print(e)
        retry_count += 1
    return power_dict
   
                
def main():
    read_energy_meter_registers(1)

if __name__ == '__main__':
    main()
        

