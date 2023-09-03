import sys
sys.path.append('/home/pi/smarteye/data/flowmeter')
sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
from datetime import datetime as dt
import smartgen.energy_meter_data_converter as energy_meter_data_converter
import main_energy_meter as dpm_reader

def get_dpm_data(equipment_data,power_meter_config):
    energy_meter_register = dpm_reader.read_energy_meter_registers(address,equipment)
    if not energy_meter_register:
        return
    ct=dt.datetime.now()
    current_time = ct.strftime('%Y-%m-%d %H:%M:%S')
    print('date time is: {}'.format(current_time))
    energy_dict={"timestamp":current_time,"mac_address":get_mac_address()}
    energy_meter_payload=energy_meter_register.copy()
    energy_meter_payload.update(energy_dict)
    if flowmeter_data:
        