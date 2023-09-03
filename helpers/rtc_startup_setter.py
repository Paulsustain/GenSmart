import os
import subprocess

def set_time_from_rtc():
    os.system('sudo hwclock -s')
    
if __name__=="__main__":
    set_time_from_rtc()
