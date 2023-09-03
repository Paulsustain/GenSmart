import time
import sys
import json
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service
import remote_upload_service


import datetime
        
def update_dfm_with_remote_config():
    #1. Get remote config
    try:
        config_dict = remote_upload_service.get_device_config()
    except:
        print('error connecting to api')
        return
    print(config_dict)
    #2. Get current local config
    local_flowmeter_config = json.loads(sqlite_service.get_dfm_config_by_slug('FLOWMETER_DETAILS'))
    #3. Update the local config if it differs from the remote config
    local_powermeter_config = json.loads(sqlite_service.get_dfm_config_by_slug('POWERMETER_DETAILS'))
    if config_dict:
        flowmeter_config = config_dict['flowmeter_details']
        print(flowmeter_config)
        if flowmeter_config and flowmeter_config != local_flowmeter_config:
            print('New flowmeter configurations')
            print('local: {}\n'.format(local_flowmeter_config))
            print('remote: {}\n'.format(flowmeter_config))
            sqlite_service.update_dfm_config('FLOWMETER_DETAILS', json.dumps(flowmeter_config))
            
        powermeter_config = config_dict['powermeter_details']
        print(powermeter_config)
        if powermeter_config and powermeter_config != local_powermeter_config:
            print('New powermeter configurations')
            print('local: {}\n'.format(local_powermeter_config))
            print('remote: {}\n'.format(powermeter_config))
            sqlite_service.update_dfm_config('POWERMETER_DETAILS', json.dumps(powermeter_config))
        
    #4. 
def main():
    update_dfm_with_remote_config()

if __name__ == '__main__':
    main()
