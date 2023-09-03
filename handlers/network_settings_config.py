
import os
import subprocess
def setup_network_interface():
    original_filename='dhcpcd.conf'
    renamed_filename='dhcpcd.conf.old'
    dir='/etc/'
    new_network_config_path='/home/pi/smarteye/crons/'+original_filename
    if not os.path.exists(dir+renamed_filename):
        try:    
            print('got to sudo mv')
            print(dir+original_filename)
            print(dir+renamed_filename)
            subprocess.run(["sudo","mv",dir+original_filename,dir+renamed_filename])
            subprocess.run(["sudo","cp",new_network_config_path, dir])
            print("network config moved successfully")
            #shutil(dir+filename,file_dir)
        except Exception as e:
            print(e)
            print('unable to complete network config')
    else:
        print("Network configuration already done")

if __name__ == "__main__":
    setup_network_interface()