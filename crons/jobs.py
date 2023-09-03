import os
import subprocess

from crontab import CronTab

#CWD = os.path.dirname(os.path.realpath(__file__))

CWD = "/home/pi/smarteye/crons"

"""
The purpose of this module is to handle cron jobs in the application

1. This module runs other crons in the atg folder and/or the flowmeter folder as the case may be
2. This module also adds general services that affect the entire application, irrespective of whether it is atg or flowmeter
"""
def main():
    """
    This is the main function, this function runs other function within the module
    """
    run_general_jobs()
    run_jobs()
    setup_daemon('i2c_rtc.service')
    setup_daemon('lcd_display.service')
    
def run_general_jobs():
    """
    This function adds general crons, that runs for the entire application
    """
    my_cron = CronTab(user='pi')

    my_cron.remove_all() # remove all crons first
    my_cron.write() # start writing new crons

    #rewrite static jobs
    #cron to handle sim reboot when device is starting up
    job = my_cron.new(command='python3 /home/pi/smarteye/helpers/sim_reboot.py', comment = 'sim_reboot')
    job.every_reboot()
    #sim module will reboot
    
    #cron to handle firmware download when device is starting up ---not working
    job = my_cron.new(command='python3 /home/pi/firmware_download_manager.py', comment = 'download_manager')
    job.every_reboot()
    #
    #cron to handle sim module reboot
    job = my_cron.new(command='python3 /home/pi/smarteye/helpers/sim_reboot.py', comment = 'sim_reboot')
    job.minute.every(30)
    #sim module will reboot

    #cron to handle device restart to prevent freeezing from overwork
    job = my_cron.new(command='python3 /home/pi/smarteye/helpers/pi_restart.py' , comment = 'pi_restart')
    #job.hours.every(12)
    job.every(6).hours()
    
    # cron to handle device heartbeat
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/heartbeat_handler.py', comment = 'heartbeat_handler')
    job.minute.every(1)
    
    #cron to handle firmware upgrade ---not working
    job = my_cron.new(command='python3 /home/pi/firmware_download_manager.py' , comment = 'download_manager')
    job.minute.every(24)
    
    #cron to handle anydesk config at reboot
    job = my_cron.new(command='python3 /home/pi/smarteye/handlers/anydesk_config.py', comment = 'anydesk_config')
    job.every_reboot()
    
    #cron to handle network config at reboot
    job = my_cron.new(command='python3 /home/pi/smarteye/handlers/network_settings_config.py', comment = 'network_config')
    job.every_reboot()
    
    #cron to update RTC time with internet time
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/rtc_update_handler.py', comment = 'rtc_update_handler')
    job.minute.every(5)

    #cron to pull remote changes from master every 45 minutes
##    job = my_cron.new(command='python3  /home/pi/smarteye/puller.py', comment = 'remote_changes_puller')
##    job.minute.every(45)

    
    #job = my_cron.new(command='python3  /home/pi/smarteye/helpers/rtc_startup_setter.py', comment = 'rtc_startup_setter')
    #job.minute.every(1)
    

    my_cron.write()
    for job in my_cron:
        print(job)        
        
def run_jobs():
    #get current dir
    """
    This function checks for jobs.py within folders in its directory, if there are any, it runs them.
    
    This allows it to write jobs for both flowmeter and atg
    """
    try:
        print('this is the CWD: {}'.format(CWD))
        #return a list of dirs in the dir
        print(os.listdir(CWD))
        # dirs = [dir for dir in os.listdir(CWD) if os.path.isdir(dir)] # previous code--- no longer working due to upgrade
        dirs = [dir for dir in os.listdir(CWD) if os.path.isdir(os.path.join(CWD, dir))] # new code tested okay
        # for each dir, run the jobs.py file
        print(dirs)
        for dir in dirs:
            job_path = CWD + "/" + dir + "/jobs.py"
            print(job_path)
            if os.path.exists(job_path):
                print('got here')
                process = subprocess.run(['/usr/bin/python3', job_path], stdout=subprocess.PIPE, universal_newlines=True)
                print("inside "+job_path)
                print(process.stdout)
    except Exception as e:
        print(e)


 
def setup_daemon(filename):
    """
    This function adds a service to systemd, it accepts the file name within its directory and adds the file to systemd as a service
    """
    dir = '/etc/systemd/system/'
    if not os.path.exists(dir+filename):
        filepath = CWD+ '/' + filename
        if os.path.exists(filepath):
            os.system("sudo cp {} {}".format(filepath, dir))
            os.system("sudo systemctl daemon-reload")
            os.system("sudo systemctl start {}".format(filename))
            os.system("sudo systemctl enable {}".format(filename))
        else:
            print("Filename doesn't exist in this directory")
    else:
        print("Service has already been registered")

        
if __name__ == "__main__":
    main()