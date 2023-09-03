from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces

def get_device_mac_address():
    address = netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr']
    #address="b8:27:eb:fb:31:fc"
    return address

def get_device_ip_address():
	address = 'nil'
	try : 
		address = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
	except:
		print('lan ip not found')

	if(address == 'nil'):
		try:
			address = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
		except:
			print('wifi ip  not found')
	
	if(address == 'nil'):
		try:
			address = netifaces.ifaddresses('ppp0')[netifaces.AF_INET][0]['addr']
		except:
			print('wifi ip  not found')
			
	return address
