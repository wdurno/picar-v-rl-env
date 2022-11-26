from flask import Flask 
from PIL import Image 
import numpy as np 
import json 
from time import time, sleep 
from car import img, find_blob, fw, bw, pan_servo, tilt_servo  
## primary car interface:
## - img ## img.read(), img.release()
## - find_blob() ## returns (x, y), radius
## - fw ## front wheels, ie. fw.turn(90)
## - bw ## back wheels, ie. bw.speed = 60, bw.stop(), bw.forward()

TURN_ANGLE_CENTER = 90 
TURN_ANGLE_DELTA = 45 
MOTOR_SPEED = 40 
DRIVE_TIME = .5 ## seconds 
PAN_CENTER = 80 
TILT_CENTER = 20 
PAN_TILT_DELTA = 30 

app = Flask(__name__) 

@app.route('/') 
@app.route('/health') 
def health(): 
    return 'PiCar-V API is functional', 200 

@app.route('/img') 
def get_img(): 
    successful_read, i = img.read() 
    if not successful_read: 
        raise Exception('`img.read()` failed!') 
    i = np.array(Image.fromarray(i).resize((60, 80))) 
    return json.dumps(i.tolist()), 200 

@app.route('/drive-left') 
def drive_left(): 
    __turn_and_drive(turn_angle=TURN_ANGLE_CENTER - TURN_ANGLE_DELTA) 
    return 'drive-left', 200 

@app.route('/drive-right') 
def drive_right(): 
    __turn_and_drive(turn_angle=TURN_ANGLE_CENTER + TURN_ANGLE_DELTA) 
    return 'drive-right', 200 

@app.route('/drive-forward') 
def drive_forward(): 
    __turn_and_drive(turn_angle=TURN_ANGLE_CENTER) 
    return 'drive-forward', 200

@app.route('/drive-backward') 
def drive_backward(): 
    __turn_and_drive(turn_angle=90, drive_forward=False) 
    return 'drive-backward', 200 

@app.route('/look-left') 
def look_left(): 
    __look(PAN_CENTER + PAN_TILT_DELTA, TILT_CENTER) 
    return 'look-left', 200 

@app.route('/look-right') 
def look_right(): 
    __look(PAN_CENTER - PAN_TILT_DELTA, TILT_CENTER) 
    return 'look-right', 200 

@app.route('/look-up') 
def look_up(): 
    __look(PAN_CENTER, TILT_CENTER + PAN_TILT_DELTA) 
    return 'look-up', 200 

@app.route('/look-forward') 
def look_forwad(): 
    __look(PAN_CENTER, TILT_CENTER)
    return 'look-forward', 200 

def __turn_and_drive(turn_angle=120, drive_time=DRIVE_TIME, motor_speed=MOTOR_SPEED, drive_forward=True): 
    fw.turn(turn_angle) 
    bw.speed = motor_speed 
    if drive_forward: 
        bw.backward() ## my motors are up-side-down :( 
    else: 
        bw.forward() 
        pass
    sleep(drive_time) ## waint until drive time elapses 
    bw.stop() 
    fw.turn(90) 
    pass 

def __look(pan_angle=80, tilt_angle=20): 
    pan_servo.write(pan_angle) 
    tilt_servo.write(tilt_angle) 
    pass 

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) 
    pass 

