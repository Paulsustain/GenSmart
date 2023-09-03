from crontab import CronTab
import sys
import json
import os
import subprocess
sys.path.append('/home/pi/smarteye/services/atg')
import sqlite_service

"""
The purpose of this module is to add cron jobs peculiar to only ATG

***caveat***

Running this module directly will lead to doubling of the cron jobs here. So, run from the main jobs.py in /home/pi/smarteye/crons
"""
def install_new_jobs():
    
    """
    This function write jobs peculiar to ATG alone
    """
    my_cron = CronTab(user='pi')
    
    #my_cron.remove_all()
    my_cron.write()
    
    # cron handles pushing inventory logs in the atg_primary_log table to remote server every minute
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/remote_logger_handler.py', comment = 'inventory_handler')
    job.minute.every(1)
    
    # cron handles tls delivery checks every minute
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/remote_tls_delivery_handler.py', comment = 'tls_delivery_handler')
    job.minute.every(1)
    
    #  cron handles pushing inventory logs in the hydrostatic sensor type of probe 
    job = my_cron.new(command ='python3 /home/pi/smarteye/handlers/atg/sensor_remote_logger_handler.py', comment='remote_sensor_handler')
    job.minute.every(1)

    # cron handles checking of remote configuration from remote server
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/remote_config_updater_handler.py', comment = 'remote_config_updater_handler')
    job.minute.every(1)


    #get new transmit interval and reset jobs
    interval= json.loads(sqlite_service.get_device_config_by_slug('DEVICE_DETAILS')[0])['transmit_interval']
    
    local_transmit_interval = interval//60
    if local_transmit_interval < 1:
        local_transmit_interval = 1

    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/tls_data_logger_handler.py', comment = 'tls_data_logger_handler')
    job.minute.every(2)
    
##    job = my_cron.new(command='python3 /home/pi/smarteye/handlers/atg/sensor_data_logger_handler.py', comment = 'sensor_data_logger_handler')
##    job.minute.every(local_transmit_interval)
##    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/multicont_data_logger_handler.py', comment = 'multicont_data_logger_handler')
##    job.minute.every(local_transmit_interval)
    #query delivery every 1 minute
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/tls_delivery_handler.py', comment = 'tls_delivery_handler')
    job.minute.every(2)
    
    #read italiana every 2 minutes
##    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/atg/italiana_data_logger_handler.py', comment = 'italiana_data_logger_handler')
##    job.minute.every(2)
    job = my_cron.new(command='python3 /home/pi/smarteye/handlers/atg/RS485_probes_handler.py', comment = 'RS485_probes_handler')
    job.minute.every(2)
    
    my_cron.write()

    for job in my_cron:
        print(job)
        
def setup_udev_rule(filename):
    faker=filename
    dir='/home/pi/smarteye/crons/atg/'
    file_dir = '/etc/udev/rules.d/'
    if not os.path.exists(file_dir+filename):
        try:    
            print('got to sudo cp')
            subprocess.run(["sudo","cp",dir+filename,file_dir])
            subprocess.run(["sudo","udevadm","trigger"])
            
            #shutil(dir+filename,file_dir)
        except:
            print('unable to create atg udev rule')
    else:
        print("atg udev has already been registered")

def main():
    """
    This is the main function, it runs other functions within the module
    """
    install_new_jobs()
    setup_udev_rule('atg_custom_udev.rules')

if __name__ == '__main__':
    main()
