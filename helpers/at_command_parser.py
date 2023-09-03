import re
import time
import sys
sys.path.append('/home/pi/smarteye/handlers')
import at_command_handler as handler

def network_provider_parser(text):
    network = 'Unknown'

    if re.compile('|'.join(['econet', 'airtel']), re.IGNORECASE).search(text):
        network = 'Airtel'

    if re.compile('|'.join(['mtn']), re.IGNORECASE).search(text):
        network = 'MTN'
        
    if re.compile('|'.join(['glo', 'globacom']), re.IGNORECASE).search(text):
        network = 'GLO'

    if re.compile('|'.join(['etisalat', '9mobile']), re.IGNORECASE).search(text):
        network = '9mobile'

    return network

def phone_number_parser(text):
    pattern = '\d{11,}'
    phone_number = re.findall(pattern, text)

    if phone_number:
        return phone_number[0]
    else:
        return "Error parsing phone number"

def data_balance_parser(serialConn, text):
    pattern = '\d+\.*\d*MB'
    if 'CMTI' in text:
        #extract message index
        cmti_text = re.search('CMTI:(.*)', text).group()
        index = re.findall('\d+',cmti_text)
        if index:
            index = index[0]
        else:
            return "Error finding sms index"
        #read message
        message = handler.sms_reader(serialConn, index)
        message_clean = re.sub('[\r\n]',' ', message)
        data_balance = re.findall(pattern, message_clean)
        if data_balance:
            return data_balance[0]
        else:
            return "Error parsing data balance from SMS"
    else:
        data_balance = re.findall(pattern, text)
        if data_balance:
            return data_balance[0]
        else:
            return "Error parsing data balance from USSD"
        

def airtime_balance_parser(text):
    pass

def signal_strength_parser(text):
    #SIGNAL CONVERSIONS
    signal_permitted_values = list(range(31))
    signal_permitted_rssi = [val*2-113 for val in signal_permitted_values]
    
    text = text.split(':')
    if text:
        text = text[1]
    else:
        return "Error 1 parsing signal strength"
    
    signal_params = text.split(',')
    if signal_params:
        RSSI_value = int(signal_params[0]) #Received Signal Strength Indicator
        #BER = int(signal_params[1]) #Channel Bit Error Rate
    else:
        return "Error 2 parsing signal strength"
        
    
    #Get Signal condition
    if 0<=RSSI_value<=9:
        signal_condition = 'Marginal'
    elif 10<=RSSI_value<=14:
        signal_condition = 'Okay'
    elif 15<=RSSI_value<=19:
        signal_condition = 'Good'
    elif 20<=RSSI_value<=30:
        signal_condition = 'Excellent'
    elif RSSI_value>30:
        signal_condition = 'Excellent'
    else:
        signal_condition = 'Unknown'

    #Get RSSI in dBM
    if RSSI_value <= 30:
        RSSI_dbm = signal_permitted_rssi[signal_permitted_values.index(RSSI_value)]
    else:
        RSSI_dbm = signal_permitted_rssi[-1]
    signal_dict = {"Signal_level(dBm)":str(RSSI_dbm)+'dB', "Signal_condition":signal_condition, "Signal_value(0-30)":RSSI_value}

    return signal_dict
