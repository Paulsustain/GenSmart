import os
import subprocess
from datetime import datetime
from subprocess import run,PIPE
from time import sleep
file_path = "/home/pi/smarteye/helpers/rtc_logs.txt"


def set_time_from_rtc():
    """
    this function compares real-time-clock(RTC) module time with the Raspberry-PI time in order to maintain accurate time in the database.
    """
    while True:
        try:
            pi_time,hardware_time,difference=get_time_data()
            if abs(difference)> 30:
                subprocess.run(['sudo', 'hwclock' ,'-s']) #s=set
                pi_time,hardware_time,difference=get_time_data()
                print('hardware time is: {} while Pi time is {}  and difference is: {} \n'.format(hardware_time,pi_time,difference))
                if abs(difference) > 30:
                    set_time_manually(hardware_time)
                with open(file_path, "a") as myfile:
                    myfile.write('hardware time is: {} while Pi time is {}  and difference is: {} : automatically\n'.format(hardware_time,pi_time,difference))
                print('time set autmatically')
            else:
                print('time difference is within 30 seconds')
        except Exception as e:
            with open(file_path, "a") as myfile:
                myfile.write('failed with exception: \n {}'.format(e))
            print(e)
        sleep(10)
        
	
def get_time_data():
    """
    This function returns the accurate time after comparison between RTC & Raspberry-PI time.
    """
    res=subprocess.run(['sudo', 'hwclock' ,'-r'],stdout=PIPE) #r=run
    splitted=str(res.stdout).split('+') 
    hardware_time=splitted[0][2:]
    hardware_time=datetime.strptime(hardware_time,'%Y-%m-%d %H:%M:%S.%f')
    print(hardware_time)
    pi_time=datetime.now()
    difference=(pi_time-hardware_time).total_seconds()
    print(difference)
    return (pi_time,hardware_time,difference)


def set_time_manually(hardware_time):
    res=subprocess.run(['sudo','date','-s',hardware_time],stdout=PIPE)
    with open(file_path, "a") as myfile:
            myfile.write('hardware time is: {}, result is: {} manually\n'.format(hardware_time,res.stdout))
    print('time set manually')
    
if __name__=="__main__":
    set_time_from_rtc()
