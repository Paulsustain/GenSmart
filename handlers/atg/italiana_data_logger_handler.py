import sys
sys.path.append('/home/pi/smarteye/data/probe')
sys.path.append('/home/pi/smarteye/services/atg')
sys.path.append('/home/pi/smarteye/helpers/atg')
import italiana_probe_address as probes_addresses
import main_italiana as probe
import sqlite_service
from datetime import datetime
import helper
import get_pv_flag

"""
The general function of this script is to push queried Start-Italiana logs to the local database(SQLite).
"""

def data_handler():
    addresses=probes_addresses.get_addresses()
    for address in addresses:
        probe_data=probe.read_probe(address)
        if not probe_data: continue
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(timestamp, ' ' ,probe_data)
        mac_address=helper.get_device_mac_address()
        device_data={'mac_address':mac_address,'read_at':timestamp,'controller_type':'STL','tank_index':address}
        combined_data=probe_data.copy()
        combined_data.update(device_data)
        pv_flag=get_pv_flag.pv_flag(combined_data)
        combined_data['pv_flag']=pv_flag
        print(combined_data)
        if combined_data['probe_address'] != str(address):
            continue
        sqlite_service.italiana_probe_insert_one(combined_data)
        sqlite_service.update_tank_latest_reading_italiana(combined_data)
if __name__ =='__main__':
    data_handler()