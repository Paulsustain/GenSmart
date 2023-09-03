import time
import sys
import package_manager
import os
import datetime
sys.path.append('/home/pi/smarteye/services') 
import sqlite_service
import mysql_remote_logger
import subprocess

def control_device_firmware_version():
    time.sleep(60)
    try:
        version= sqlite_service.get_device_config_by_slug('FIRMWARE_VERSION')
        local_version = ''
        for (value) in version: 
            local_version = (value[0])
        
        version_dict = mysql_remote_logger.get_device_expected_version()
        print(version_dict)
        if(version_dict["expected_version_number"] != None and version_dict["expected_version_number"] != ""
         and version_dict["expected_version_number"] != local_version):
            print('not same, requires update')
            config_dict = mysql_remote_logger.get_latest_firmware_version_details(version_dict["expected_version_number"])
            if(config_dict["version_number"] != None and config_dict["version_number"] != ""):
                print('downloading new version')
                download_and_install_new_firmware(config_dict["version_number"],config_dict["file_name"],config_dict["download_link"] )
        else:
	        #no need to install new, just update remote
            print('no update required')
            mysql_remote_logger.send_current_firmware_version_to_remote_server(local_version)

    except:
        #2+ffff+'edddd'
        print("could not get or update device firmware version")


def download_and_install_new_firmware(version_number,file_name, download_link):
    FILE_UNZIP_CONFIRMATION_TEXT = ''

    os.system("sudo rm -r __MACOSX/")
    os.system("sudo rm -rf  ./smarteye_bk")
    os.system("sudo mkdir  ./smarteye_bk")
    os.system("sudo cp -r  ./smarteye/. ./smarteye_bk")
    os.system("sudo rm "+file_name+".zip")
    os.system("sudo rm -rf ./download_room")
    os.system("sudo wget " +download_link)
    exists = os.path.isfile("/home/pi/"+file_name+".zip")
    if exists:
        print("file downloaded successfully")
    else: 
        print("no zip file downloaded")
        sys.exit()
    os.system("sudo unzip "+file_name+".zip -d  ./download_room")
    if(file_name != 'smarteye'):
        os.system("sudo mv  ./download_room/"+ file_name+ " ./download_room/smarteye")

    TEXT = ''
    process = subprocess.Popen(['cat', 'download_room/smarteye/unzip_checker.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    TEXT = stdout

    if(TEXT !=  b'print(1)\n'  ):
        print("unzip not successful, exiting")
        sys.exit()

    os.system("sudo cp --remove-destination  ./smarteye_bk/db/store.db ./download_room/smarteye/db")
    os.system("sudo python3 ./download_room/smarteye/package_manager.py")
    if(package_manager.recheck_installed_packages() == 'exit_firmware_update'):
        print("package update not successful, exiting")
        sys.exit()

    os.system("sudo python3 ./download_room/smarteye/db/migrations.py")
    os.system("sudo python3 ./download_room/smarteye/crons/jobs.py")
    os.system("sudo rm -rf ./smarteye")
    os.system("sudo mv ./download_room/smarteye  ./smarteye")
    os.system("sudo chown -R pi:pi ./smarteye")
    os.system("sudo cp --remove-destination  ./smarteye/firmware_download_manager.py  ./")
    os.system("sudo cp --remove-destination  ./smarteye/package_manager.py  ./")

    sqlite_service.update_device_firmware_version(version_number)
    mysql_remote_logger.send_current_firmware_version_to_remote_server(version_number)

def main():
    control_device_firmware_version()
 

if __name__ == '__main__':
    main()
