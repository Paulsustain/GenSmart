import sys
sys.path.append('/home/pi/smarteye/services/atg')
import remote_api_service

def log_data_to_remote_api():
    try:
        remote_api_service.upload_delivery_log()
    except:
        print("could not log tls deliveries to remote db")

def main():
    log_data_to_remote_api()

if __name__ == '__main__':
    main()

