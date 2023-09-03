import sys
sys.path.append('/home/pi/smarteye/publishers')
import emit_heartbeat

def send_heartbeat_message_to_remote_server():
    try:
        emit_heartbeat.send_heartbeat_message_to_remote_server()
    except:
        print("heartbeat message not sent")

def main():
    send_heartbeat_message_to_remote_server()

if __name__ == '__main__':
    main()
