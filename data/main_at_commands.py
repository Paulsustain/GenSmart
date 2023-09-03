import serial
import time
import os
import datetime
import sys
sys.path.append('/home/pi/smarteye/helpers')
import helper
from custom_decorators import retry
sys.path.append('/home/pi/smarteye/handlers')
import at_command_handler as handler
sys.path.append('/home/pi/smarteye/services/atg')
from services import sqlite_service

@retry(retry_count=3, delay=10)

def main():
    gprs_conn = ["sudo poff gprs_connect", "sudo pon gprs_connect"] #This is used to reset the sim-module in the case of a poor connection.
    gprs_port = "/dev/ttyAMA0"
    MAC = helper.get_device_mac_address()
    os.system(gprs_conn[0])
    time.sleep(1)
    #Setup serial communication
    conn = serial.Serial(gprs_port, baudrate=115200)
    conn.reset_output_buffer()
    #main thread
    network = handler.network_checker(conn)
    time.sleep(1)
    signal = handler.signal_strength_checker(conn)
    time.sleep(1)
    if network!='Unknown':
        if network == 'Airtel':
            data_balance = handler.data_balance_checker(conn, network)
            time.sleep(1)
            airtime_balance = handler.airtime_balance_checker(conn, network)
            time.sleep(1)
            number = handler.phone_number_checker(conn, network)
        else:
            data_balance = handler.data_balance_checker(conn, network)
            time.sleep(1)
            airtime_balance = handler.airtime_balance_checker(conn, network)
            time.sleep(1)
            number = handler.phone_number_checker(conn, network)
            
            

    payload = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Network_provider":network,
        "Data_balance": data_balance,
        "Phone_number": number,
        "Signal_details": signal,
        "device_address": MAC,
        "Airtime_balance": airtime_balance
    }
    print(payload)
    sqlite_service.update_at_command_info(payload)
    os.system(gprs_conn[1])
    time.sleep(1)
    conn.close()
    
    return True

if __name__ == "__main__":
    main()
