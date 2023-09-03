# import serial
import sys
sys.path.append('/home/pi/smarteye/helpers')
import at_command_parser as parser
import time
 

#------------------Global AT command variables---------------------
AT_variables = {
    "Prefix": 'AT+',
    "Terminator": '\r\n',
    "network_provider_1": 'CSPN?',
    "network_provider": 'COPS?',
    "USSD": 'CUSD=1',
    "signal_strength": 'CSQ',
    "read_sms": 'CMGR=',
    "sms_text_format": 'CMGF=1',
}
#--------------------------------------------------------------------

def network_checker(serialConn):
    command_1 = AT_variables["Prefix"]+AT_variables["network_provider_1"]+AT_variables["Terminator"]
    serialConn.write(command_1.encode())
    time.sleep(1)
    command = AT_variables["Prefix"]+AT_variables["network_provider"]+AT_variables["Terminator"]
    serialConn.write(command.encode())
    time.sleep(1)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()
    network = parser.network_provider_parser(rcv)
    return network


def phone_number_checker(serialConn, network_provider):
    rcv = None

    ussd_codes = {
        "airtel": '"*121*3*4#"',
        "mtn": '"*663#"',
        "glo": '"*135*8#"',
        "9mobile": '"*248#"'
    }
    
    command = AT_variables["Prefix"]+AT_variables["USSD"]+','+ussd_codes[network_provider.lower()]+AT_variables["Terminator"]
    serialConn.write(command.encode())
    time.sleep(5)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()
##    return rcv 
    phone_number = parser.phone_number_parser(rcv)
    return phone_number


def data_balance_checker(serialConn, network_provider):
    rcv = None

    ussd_codes = {
        "airtel": '"*141*11*0#"',
        "mtn": '"*131*4#"',
        "glo": '"*127*0#"' ,
        "9mobile": '"*200*3*2#"'
    }
    
    command = AT_variables["Prefix"]+AT_variables["USSD"]+','+ussd_codes[network_provider.lower()]+AT_variables["Terminator"]
    serialConn.write(command.encode())
    time.sleep(10)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()
    return rcv
##    data = parser.data_balance_parser(serialConn, rcv)       
##    return data

def airtime_balance_checker(serialConn, network_provider):
    rcv = None

    ussd_codes = {
        "airtel": '"*123#"',
        "mtn": '"*556#"',
        "glo": '"#124*1#"' ,
        "9mobile": '"*232#"'
    }
    
    command = AT_variables["Prefix"]+AT_variables["USSD"]+','+ussd_codes[network_provider.lower()]+AT_variables["Terminator"]
    serialConn.write(command.encode())
    time.sleep(5)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()
    
    return rcv

def signal_strength_checker(serialConn):
    rcv = None

    command = AT_variables["Prefix"]+AT_variables["signal_strength"]+AT_variables["Terminator"]
    serialConn.write(command.encode())
    time.sleep(1)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()
  
    signal = parser.signal_strength_parser(rcv)
    return signal

def sms_reader(serialConn, index):
    init_command = AT_variables["Prefix"]+AT_variables["sms_text_format"]+AT_variables["Terminator"]
    command = AT_variables["Prefix"]+AT_variables["read_sms"]+index+AT_variables["Terminator"]
    serialConn.write(init_command.encode())
    time.sleep(2)
    serialConn.write(command.encode())
    time.sleep(5)
    rcv = serialConn.read(size=serialConn.in_waiting)
    
    rcv = rcv.decode()

    return rcv
