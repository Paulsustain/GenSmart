import italiana_data_logger_handler as italiana
import multicont_data_logger_handler as multicont
import sensor_data_logger_handler as hydrostatic
import gamicos_data_logger_handler as gamicos
from time import sleep

def probes_handler():
    gamicos.data_handler()
    print('*****gamicos ran*****')
    sleep(0.5)
    hydrostatic.log_sensor_data_to_db()
    print('*****hydrostatic ran, italiana next*****')
    sleep(0.5)
    italiana.data_handler()
    print('*****italiana ran, multicont next*****')
    sleep(0.5)
    multicont.get_mtc_data()
    print('*****multicont ran*****')
  

if __name__ =='__main__':
    probes_handler()