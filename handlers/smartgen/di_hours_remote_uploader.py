import sys
sys.path.append('/home/pi/smarteye/services/smartgen')
import remote_upload_service as rs

def main():
    rs.upload_di_hours()

if __name__ == '__main__':
    main()
