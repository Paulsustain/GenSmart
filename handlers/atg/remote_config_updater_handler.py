import time
import sys
import json
sys.path.append('/home/pi/smarteye/crons')
sys.path.append('/home/pi/smarteye/handlers')
import firmware_upgrade_routine
import jobs
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service
import remote_api_service


import datetime
        
def update_device_with_remote_config():
    #1. Get remote config
    try:
        config_dict = remote_api_service.get_device_config()
        print(config_dict)
    except:
        print('error connecting to api')
        return
    #2. Get current local config
    local_tank_config = json.loads(sqlite_service.get_device_config_by_slug('TANK_DETAILS')[0])
    local_device_config = json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])
    #3. Update the local config if it differs from the remote config
    if config_dict:
        tank_config = config_dict['tank_details']
        device_config = config_dict['device_details']
        print(tank_config)
        if tank_config != local_tank_config:
            print('New tank configurations')
            print('local: {}\n'.format(local_tank_config))
            print('remote: {}\n'.format(tank_config))
            sqlite_service.new_update_device_config('TANK_DETAILS', json.dumps(tank_config))
            
        if device_config != local_device_config:
            print('New device configurations')
            print('local: {}\n'.format(local_device_config))
            print('remote: {}\n'.format(device_config))
            sqlite_service.new_update_device_config('DEVICE_DETAILS', json.dumps(device_config))
            
            if device_config['transmit_interval'] > 0 and device_config['transmit_interval'] != local_device_config['transmit_interval']:
                jobs.main()
            
        
    #4. 
def main():
    update_device_with_remote_config()

if __name__ == '__main__':
    main()
