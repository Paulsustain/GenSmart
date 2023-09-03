from crontab import CronTab
import sys
import os
import subprocess
import shutil
base_dir = os.path.dirname(os.path.realpath(__file__))

def setup_daemon(filename):
    dir = '/etc/systemd/system/'
    if not os.path.exists(dir+filename):
        filepath = base_dir + '/' + filename
        if os.path.exists(filepath):
            os.system("sudo cp {} {}".format(filepath, dir))
            os.system("sudo systemctl daemon-reload")
            os.system("sudo systemctl start {}".format(filename))
            os.system("sudo systemctl enable {}".format(filename))
        else:
            print("Filename doesn't exist in this directory")
    else:
        print("Service has already been registered")

def setup_udev_rule(filename):
    faker=filename
    dir='/home/pi/smarteye/crons/smartgen/'
    file_dir = '/etc/udev/rules.d/'
    if not os.path.exists(file_dir+filename):
        try:    
            print('got to sudo cp')
            subprocess.run(["sudo","cp",dir+filename,file_dir])
            subprocess.run(["sudo","udevadm","trigger"])
            #shutil(dir+filename,file_dir)
        except:
            print('unable to create dfm udev rule')
    else:
        print("dfm udev has already been registered")
        
def setup_daemons():
    setup_daemon('di_hours.service')
    setup_udev_rule('dfm_custom_udev.rules')
            
    
def install_new_jobs():
    my_cron = CronTab(user='pi')

    #my_cron.remove_all()
    my_cron.write()
    
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/smartgen/dfm_remote_uploader.py', comment = 'dfm_remote_upload')
    job.minute.every(2)
    
    job = my_cron.new(command='python3  /home/pi/smarteye/handlers/smartgen/di_hours_remote_uploader.py', comment = 'di_hours_remote_upload')
    job.minute.every(2)
    
    job = my_cron.new(command='python3  /home/pi/smarteye//handlers/smartgen/dfm_handler.py', comment = 'dfm_logger')
    job.minute.every(1)
    my_cron.write()

    for job in my_cron:
        print(job)

def main():
    install_new_jobs()
    setup_daemons()

if __name__ == '__main__':
    main()

