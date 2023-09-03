import os
import time
import datetime as dt

def main():
    file_path = "/home/pi/smarteye/helpers/reboot_logs.txt"
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "a") as myfile:
        myfile.write(timestamp + '\n')
    os.system("sudo reboot")
    #time.sleep(2)

if __name__ == '__main__':
    main()
