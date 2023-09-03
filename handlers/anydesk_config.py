import os
import subprocess

"""
The function of this script is to rename the service.conf file located at '/etc/anydesk'. This will be forced to generate a new Anydesk
ID.
"""

def run_anydesk_setup():
    original_filename='service.conf'
    renamed_filename='service.conf.old'
    dir='/etc/anydesk/'
    if not os.path.exists(dir+renamed_filename):
        try:    
            print('got to sudo mv')
            print(dir+original_filename)
            print(dir+renamed_filename)
            subprocess.run(["sudo","mv",dir+original_filename,dir+renamed_filename])
            subprocess.run(["sudo","systemctl","restart", "anydesk"])
            print("Anydesk config file renamed successfully")
            #shutil(dir+filename,file_dir)
        except:
            print('unable to rename Anydesk config file')
    else:
        print("Anydesk config file already renamed")
        
if __name__=='__main__':
    run_anydesk_setup()