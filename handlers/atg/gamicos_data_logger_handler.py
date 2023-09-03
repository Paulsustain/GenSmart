import sys
sys.path.append('/home/pi/smarteye/data/probe')
sys.path.append('/home/pi/smarteye/services/atg')
sys.path.append('/home/pi/smarteye/helpers/atg')
import main_gamicos_mag as probe_device
import sqlite_service
from datetime import datetime
import helper
import get_pv_flag
import json
from time import sleep

"""
The general function of this script is to push queried Gamicos logs to the local database(SQLite).
"""

def get_probes():
    tanks = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    print(tanks)
    probe_data=[]
    for tank in tanks:
        if tank['Tank_controller']=='GMC-485-D' or tank['Tank_controller']=='GMC-485-S' or tank['Tank_controller']=='GMC-485-U' :
            probe_data.append({'controller':tank['Tank_controller'],'address':tank['Tank_index']})
    print('this is the probe data: {} '.format(probe_data))
    return probe_data

def data_handler():
    probes=get_probes()
    for probe in probes:
        print('next probe is: {} and the address is: {}'.format(probe['controller'],probe['address']))
        probe_data=probe_device.read_probe(probe['address'],probe['controller'])
        if not probe_data:
            continue
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(timestamp, ' ' ,probe_data)
        mac_address=helper.get_device_mac_address()
        device_data={'mac_address':mac_address,'read_at':timestamp,'controller_type':probe['controller'],'tank_index':probe['address']}
        combined_data=probe_data.copy()
        combined_data.update(device_data)
        print(combined_data)
        pv_flag=get_pv_flag.pv_flag(combined_data)
        combined_data['pv_flag']=pv_flag
        print(combined_data)
        if combined_data['probe_address'] != combined_data['tank_index'] :
            continue
        sqlite_service.gamicos_mag_probe_insert_one(combined_data)
        sqlite_service.update_tank_latest_reading_gamicos(combined_data)
        sleep(1)
if __name__ =='__main__':
    data_handler()

