import sys
sys.path.append('/home/pi/smarteye/services')
import mysql_remote_logger

def send_at_command_info_to_remote_server():
    try:
        mysql_remote_logger.upload_at_command_info()
        print("AT command info sent to db")
    except:
        print("AT command info not sent")

def main():
    send_at_command_info_to_remote_server()

if __name__ == '__main__':
    main()
