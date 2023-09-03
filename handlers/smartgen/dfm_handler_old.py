import json
import time
import datetime as dt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys
sys.path.append('/home/pi/smarteye/data/flowmeter')
import main_dfm as dfm_reader
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
import smartgen.flowmeter_data_converter as flowmeter_data_converter

def get_dfm_addresses():
    flowmeter_details = json.loads(sqlite_service.get_dfm_config_by_slug('FLOWMETER_DETAILS'))
    return flowmeter_details   

def read_flowmeter():
    flowmeter_config=get_dfm_addresses()
    flowmeters=dfm_reader.read_all_dfm(flowmeter_config)
    for flowmeter in flowmeters:
        register,add,serial_number=flowmeter
        flowmeter_data_converter.process_dfm_data(register,add,serial_number)
        
def main():
    read_flowmeter()

if __name__ == '__main__':
    main()