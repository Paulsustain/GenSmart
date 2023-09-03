# two codes
# read the remote config
#check if there is flowmeter, if yes , get flowmeter details and print it
#check if there is ATG, if yes , get ATG details and print it
import sys
sys.path.append('/home/pi/smarteye/services/smartgen')
sys.path.append('/home/pi/smarteye/data')
import main_lcd as lcd_control
import sqlite_service
from datetime import datetime
from time import sleep
import json

def get_dfm_addresses():
    flowmeter_details = json.loads(sqlite_service.get_dfm_config_by_slug('FLOWMETER_DETAILS'))
    return flowmeter_details

def lcd_handler():
    try:
        equipment_addresses=get_equipment_addresses()
        equipment_status_handler(equipment_addresses)
    except Exception as e:
        print(e)
 

def get_equipment_addresses():
    equipment_addresses=[]
    dfms=get_dfm_addresses()
    if not dfms:
        return None
    for dfm in dfms:
        equipment_address=dfm['equipment']
        equipment_addresses.append(equipment_address)
    return equipment_addresses

def get_dfm_last_log_by_equipment_address(equipment_address):
    dfm_details=sqlite_service.get_dfm_last_log_by_equipment_address(equipment_address)
    if not dfm_details:
        return None
    print('dfm the engine running status is: {}'.format(dfm_details[17]))
    return dfm_details

def get_pm_last_log_by_equipment_address(equipment_address):
    pm_details=sqlite_service.get_pm_last_log_by_equipment_address(equipment_address)    #PM Data
    if not pm_details:
        return None
    print('pm the engine running status is: {}'.format(pm_details[24]))
    return pm_details

def get_flowmeter_details(equipment_address):
    engine_dfm_details=get_dfm_last_log_by_equipment_address(equipment_address)
    if not engine_dfm_details:
        return display_equipment_not_running_dfm(equipment_address)
    engine_running_status=engine_dfm_details[12]
    if  not engine_running_status:
        dfm_details={
            'equipment_address': equipment_address,
            'consumption_rate':0,
            'foward_fuel_rate':0,
            'backward_fuel_rate':0,
            'total_liters':engine_dfm_details[3],
            'mode':'OFF'
            }
        reformatted_dfm_data=format_dfm_display(dfm_details)
    else:
        dfm_details={
            'equipment_address': equipment_address,
            'consumption_rate':engine_dfm_details[10],
            'foward_fuel_rate':engine_dfm_details[7],
            'backward_fuel_rate':engine_dfm_details[8],
            'total_liters':engine_dfm_details[3],
            'mode':engine_dfm_details[13]
            }
        reformatted_dfm_data=format_dfm_display(dfm_details)
    return reformatted_dfm_data

def get_specific_pm_details(engine_pm_details):
    meter_type=engine_pm_details[23]
    pm_details=None
    equipment_address=engine_pm_details[6]
    total_current=float(engine_pm_details[13])+float(engine_pm_details[14])+float(engine_pm_details[15])   #PM Data
    average_current=total_current/3
    total_voltage=float(engine_pm_details[10])+float(engine_pm_details[11])+float(engine_pm_details[12])
    average_voltage=total_voltage/1.732
    if 'DPM' in meter_type:
        pm_details={
        'equipment_address': equipment_address,
        'total_power': float(engine_pm_details[19]),
        'average_current':average_current,
        'average_voltage':average_voltage
        }
    elif 'DPP' in meter_type:
        pm_details={
        'equipment_address': equipment_address,
        'total_power': float(engine_pm_details[5]),
        'average_current':float(engine_pm_details[3]),
        'average_voltage':float(engine_pm_details[4])
        }
    else:
        pass
    return pm_details

def get_powermeter_details(equipment_address):
    engine_pm_details=get_pm_last_log_by_equipment_address(equipment_address)
    if not engine_pm_details:
        return display_equipment_not_running_pm(equipment_address)    # needed
    engine_running_status=int(engine_pm_details[24])
    print(engine_running_status)
    if  not engine_running_status:
        print('engine not running')
        reformatted_pm_data=display_equipment_not_running_pm(equipment_address)
        #print('got here')
    else:
        print('engine running')
        pm_details=get_specific_pm_details(engine_pm_details)
        reformatted_pm_data=format_pm_display(pm_details)
    return reformatted_pm_data

def equipment_status_handler(equipment_addresses):
    for equipment_address in equipment_addresses:
        reformatted_dfm_data=get_flowmeter_details(equipment_address)
        lcd_control.write_to_lcd_screen(reformatted_dfm_data)
        #reformatted_pm_data=get_powermeter_details(equipment_address)     # Pm data disabled
        #lcd_control.write_to_lcd_screen(reformatted_pm_data)
        sleep(30)
        reformatted_dfm_data=get_flowmeter_details(equipment_address)
        lcd_control.write_to_lcd_screen(reformatted_dfm_data)
        sleep(30)
        
def display_equipment_not_running_pm(equipment_address):
    display=[]
    current_time=datetime.now().strftime("%H:%M")
    display.append({'message':'EQ: {}  TIME: {}'.format(equipment_address,current_time),'line':1,'position':0})
    display.append({'message':'NO POWER DATA ','line':3,'position':3})
    print('data to display is: {}'.format(display))
    return display

def display_equipment_not_running_dfm(equipment_address):
    display=[]
    current_time=datetime.now().strftime("%H:%M")
    display.append({'message':'EQ: {}  TIME: {}'.format(equipment_address,current_time),'line':1,'position':0})
    display.append({'message':'NO DFM DATA ','line':3,'position':4})
    print('data to display is: {}'.format(display))
    return display 

def format_pm_display(data_dict):
    display=[]
    current_time=datetime.now().strftime("%H:%M")
    display.append({'message':'EQ: {}  TIME: {}'.format(data_dict['equipment_address'],current_time),'line':1,'position':0})
    display.append({'message':'V: {:.2f} Volts'.format(data_dict['average_voltage']),'line':2,'position':0})
    display.append({'message':'I: {:.2f} Amps'.format(data_dict['average_current']),'line':3,'position':0})
    display.append({'message':'P: {:.2f} kW'.format(data_dict['total_power']),'line':4,'position':0})
    print('data to display is: {}'.format(display))
    return display       
        
def format_dfm_display(data_dict):
    display=[]
    current_time=datetime.now().strftime("%H:%M")
    display.append({'message':'EQ: {}  TIME: {}'.format(data_dict['equipment_address'],current_time),'line':1,'position':0})
    display.append({'message':'TL:{:.1f} L'.format(data_dict['total_liters']),'line':2,'position':0})
    display.append({'message':'CR: {:.2f} L/hr'.format(data_dict['consumption_rate']),'line':3,'position':0})
    display.append({'message':'Mode: {}'.format(data_dict['mode']),'line':4,'position':0})
    print('data to display is: {}'.format(display))
    return display
            
    

if __name__ == '__main__':
    lcd_handler()
    #get_dfm_last_log_by_equipment_address(1)
    #if dfm_details[17]: