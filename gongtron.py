import urllib, json, subprocess
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
from espeak import espeak

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH) # Configure for a touch sensor. If an EV3 touch sensor is connected, it will be configured for EV3 touch, otherwise it'll configured for NXT touch.

global handReset
handReset = False

def say_with_espeak(text, lang="en"):
    subprocess.call("espeak -v {0} {1}".format(lang, text), shell=True)
    
def hitTheGong():
    #BP.reset_all()
    #BP.set_motor_speed(BP.PORT_A, 0)
    global handReset
    BP.set_motor_position(BP.PORT_A, 160)
    #print BP.get_motor_status(BP.PORT_A)
    #BP.set_motor_speed(BP.PORT_A, 50)
    time.sleep(1)
    #BP.set_motor_position(BP.PORT_A, 0)
    #time.sleep(0.5)
    handReset = False
    
    #print BP.get_motor_status(BP.PORT_A)
    
    
def checkWebService():
    global handReset
    if handReset == True:
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=google"
        time.sleep(10)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print data['status']

        if data['status'] == "OK":
            #espeak.synth("Kylie and Melody finished a building out a template for Hoover Solution Inc. Great job!")
            espeak.synth(data['results'][0]['formatted_address'])
            time.sleep(10)
            hitTheGong()

def resetHandPosition():
    global handReset
    #print BP.get_sensor(BP.PORT_1)[0]
    if handReset == False:
        BP.set_motor_speed(BP.PORT_A, -25)
        if BP.get_sensor(BP.PORT_1)[0]:
            print "hit"
            BP.set_motor_speed(BP.PORT_A, 0)
            handReset = True

        
#webservice = sched.scheduler(time.time,time.sleep)

while True:
    resetHandPosition()
    checkWebService()
    #time.sleep(20)

#try:    
#    hitTheGong()
#except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
#    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.

#try:
#    speed = 0
#    BP.set_motor_speed(BP.PORT_A, speed)
#    print("Press touch sensor on port 1 to run motors")
    
#except KeyboardInterrupt: BP.reset_all()   
