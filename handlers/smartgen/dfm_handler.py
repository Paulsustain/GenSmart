import json
import time
import serial
from serial import Serial
import datetime as dt
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import sys
sys.path.append('/home/pi/smarteye/data/flowmeter')
import main_dfm as dfm_reader
import main_dpp as dpp_reader
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
sys.path.append('/home/pi/smarteye/helpers')
sys.path.append('/home/pi/smarteye/data/flowmeter')
import smartgen.flowmeter_data_converter as flowmeter_data_converter
import smartgen.dpp_data_processor as dpp_data_processor
import smartgen.dpm_data_processor as dpm_data_processor
import main_energy_meter as dpm_reader

def get_dfm_addresses():
    flowmeter_details = json.loads(sqlite_service.get_dfm_config_by_slug('FLOWMETER_DETAILS'))
    return flowmeter_details

def get_power_meter_addresses():
    power_meter_details = json.loads(sqlite_service.get_dfm_config_by_slug('POWERMETER_DETAILS'))
    return power_meter_details

def read_smartgen_data():
    flowmeter_config=get_dfm_addresses()
    power_meter_config=get_power_meter_addresses()
    serial_port = ModbusClient(method='rtu', port='/dev/DFM_SERIAL', timeout=1,baudrate=9600)
    client=Serial(port='/dev/DFM_SERIAL',baudrate=9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,timeout=1)

    print(serial_port)
    try:
        connection_status = serial_port.connect()
    except  Exception as Err:
        print("Unable to connect Serial Port\n".format(Err))
    for fm in flowmeter_config:
        flowmeter_address = fm["address"]
        equipment_id=fm["equipment"]
        serial_number = fm["serial_number"]
        print('this is the address: {}'.format(flowmeter_address))
        flowmeter_register = dfm_reader.read_dfm_registers(serial_port, flowmeter_address)
        #flowmeter_register=None
        if not hasattr(flowmeter_register,'registers'):
            flowmeter_register=None
        print(power_meter_config)
        if power_meter_config:
            read_pm=False
            for pm in power_meter_config:
                if pm["equipment"]==equipment_id and pm["meter_type"]=='DPP':
                    get_dpp_data(pm,serial_port,flowmeter_register,fm)
                    read_pm=True
                if pm["equipment"]==equipment_id and pm["meter_type"]=='DPM':
                    get_dpm_data(pm,client,flowmeter_register,fm)
                    read_pm=True
        if not read_pm:
            flowmeter_payload=flowmeter_data_converter.process_dfm_data((flowmeter_register,fm))
            print('this is the flowmeter payload and fm {} ***** {} '.format(flowmeter_payload,fm))
            if flowmeter_payload:
                flowmeter_payload['UUID']=''
                sqlite_service.dfm_logs_insert(flowmeter_payload)
                sqlite_service.update_dfm_logs_current_value(flowmeter_payload)
            

def get_dpm_data(pm,serial_port,flowmeter_register,fm):
    print('got into dpm')
    energy_meter_register = dpm_reader.read_energy_meter_registers(pm['address'],pm['equipment'])
    if not energy_meter_register:
        energy_meter_register=None
    flowmeter_data=(flowmeter_register,fm)
    print('got here')
    energy_meter_data=(energy_meter_register,pm)
    dpm_data_processor.process_registers(flowmeter_data,energy_meter_data)
    
    
def get_dpp_data(pm,serial_port,flowmeter_register,fm):
    print('got into dpp')
    power_meter_register = dpp_reader.read_power_meter_registers(serial_port, pm['address'])
    if not hasattr(power_meter_register,'registers'):
        power_meter_register=None
    flowmeter_data=(flowmeter_register,fm)
    print('got here')
    power_meter_data=(power_meter_register,pm)
    dpp_data_processor.process_registers(flowmeter_data,power_meter_data)    
        
def main():
    read_smartgen_data()

if __name__ == '__main__':
    main()
