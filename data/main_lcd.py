import sys
sys.path.append('/home/pi/smarteye/helpers/')
import RPi_I2C_driver as lcd_driver

lcd_controller = lcd_driver.lcd()
TEST_DATA=[
        {
            'message': 'Smartflow Tech',
            'line': 1,
            'position':3
            },
        {
            'message': 'Gen. Mon. System',
            'line': 2,
            'position':2
            },
        {
            'message': 'ATG System',
            'line': 3,
            'position':5
            },
        {
            'message': 'Pump Solution ',
            'line': 4,
            'position':3
            },
    ]
def write_to_lcd_screen(data_list):
    try:
        clear_lcd_screen()
        for data_dict in data_list:
            message=data_dict['message']
            line=data_dict['line']
            position=data_dict['position']
            lcd_controller.lcd_display_string_pos(message,line,position)
    except Exception as e:
        print(e)

def clear_lcd_screen():
    try:
        lcd_controller.lcd_clear()
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    write_to_lcd_screen(TEST_DATA)