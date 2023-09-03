import os
import subprocess
from time import sleep

hostname='ntp.org'
def update_rtc_time_from_internet():
    status=get_internet_status()
    if status==0:
        os.system('sudo hwclock -w')
        print('rtc time set from internet')
    else:
        print('no internet, time remains the same')
        
def get_internet_status():
    response=0
    print('program started')
    for k in range(3):
        response+=os.system('ping -c 1 '+hostname)
        print('response is: {}'.format(response))
        sleep(1)
    print(response)
    return response

if __name__=='__main__':
    update_rtc_time_from_internet()
        
