#Declare the gpio pins to be watched
#Add Event detection on each pin on every edge change
#Write an ISR that takes state on every change

import RPi.GPIO as GPIO
import sys
import time
from time import sleep
import datetime as dt

sys.path.append('/home/pi/smarteye/helpers')
from helper import get_device_mac_address as get_mac_address
from smartgen.boardProperties import board
sys.path.append('/home/pi/smarteye/services/smartgen')
import sqlite_service

lastState=None
justComingUp=True
mac_address = get_mac_address()

def state_test(channel):
    print(channel)
    print(GPIO.input(channel))
    
def getStates(channel):
    '''This is the work-horse of this function, it checks the status of the pins once any of the pins change'''
    # the variables below monitor the status of the pi
    global justComingUp,lastState
    stateList=[]
    
    # for each of the sources in the declared number of sources, get the status of the pin 
    for pin in board.source_pins:
        #since we are using pull-up, energising the input will pull down the pin and give a zero value. So we need to invert it to get actual value
        state=int(not(GPIO.input(pin)))
        stateList.append(state)
    
    #save the current value of the sources in the variable currentStatus as a tuple
    currentState=tuple(stateList)
    print(currentState)
    
    #due to bouncing of the relay, one power change always lead to multiple interrupt. So in order to prevent false logging, we need to check status is same as before. if yes, Skip
    #also take a log when the device is just coming up, this enures no log is lost.
    if currentState != lastState or justComingUp:
        if justComingUp:
            justComingUp=False
        current_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # this section stores each supply source as a new row in the database.
            for (index, state) in enumerate(currentState):
                print("this is the sourceID: {}".format(index))
                payload = (mac_address, index, state, current_time)
                print("this is the payload: ",payload)
                #Insert one Source status into the database
                sqlite_service.di_hours_logs_insert(payload)
            lastState = currentState
        except:
            print("Unable to insert to db")
    else:
        print("current state and last state are the same", "current state is ",currentState," and last state is ",lastState)


GPIO.setmode(GPIO.BCM)
for pin in board.source_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback= getStates, bouncetime=500)

getStates(True)

while True:
    #print(lastState, justComingUp)
    try:
        pass
    except KeyboardInterrupt:
        print('\ncaught keyboard interrupt!')
        GPIO.cleanup()
        
    
