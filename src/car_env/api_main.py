from flask import Flask, request 
from PIL import Image 
import numpy as np 
import json 
from time import time, sleep 
from .car import img, find_blob, find_blob_contours, fw, bw, pan_servo, tilt_servo  
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
    for _ in range(10): 
        ## claer cache 
        _ = img.read() 
        pass 
    successful_read, i = img.read() 
    if not successful_read: 
        raise Exception('`img.read()` failed!') 
    ## scan for red blobs 
    x, y, r = 0, 0, 0 
    for _ in range(10): 
        x_resize = int(request.args.get('x_resize', default=60)) 
        y_resize = int(request.args.get('y_resize', default=80))
        image = np.array(Image.fromarray(i).resize((x_resize, y_resize))) 
        if True: 
            ## Contours
            (tmp_x, tmp_y), tmp_r = find_blob_contours(image) 
        else: 
            ## Hough Circles 
            ## Too error-prone. Not using 
            (tmp_x, tmp_y), tmp_r = find_blob(image) 
            pass 
        if tmp_r > r: 
            x, y, r = tmp_x, tmp_y, tmp_r 
    ## package and return 
    return json.dumps((image.tolist(), x, y, r)), 200 

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

@app.route('/apply_vector', methods=['GET', 'POST']) 
def apply_vector():
    try:
        payload = request.get_json(silent=True) or {}
        pan = __read_float_param('pan', payload, default=0.0)
        tilt = __read_float_param('tilt', payload, default=0.0)
        turn = __read_float_param('turn', payload, default=0.0)
        drive = __read_float_param('drive', payload, default=0.0)

        __validate_range('pan', pan, -1.0, 1.0)
        __validate_range('tilt', tilt, 0.0, 1.0)
        __validate_range('turn', turn, -1.0, 1.0)
        __validate_range('drive', drive, -1.0, 1.0)

        pan_angle = __map_linear(pan, -1.0, 1.0, TURN_ANGLE_CENTER - TURN_ANGLE_DELTA, TURN_ANGLE_CENTER + TURN_ANGLE_DELTA)
        tilt_angle = __map_linear(tilt, 0.0, 1.0, TILT_CENTER, TILT_CENTER + PAN_TILT_DELTA)
        turn_angle = __map_linear(turn, -1.0, 1.0, TURN_ANGLE_CENTER - TURN_ANGLE_DELTA, TURN_ANGLE_CENTER + TURN_ANGLE_DELTA)

        __look(pan_angle=pan_angle, tilt_angle=tilt_angle)

        turn_is_non_zero = abs(turn) > 1e-6
        drive_is_non_zero = abs(drive) > 1e-6

        if turn_is_non_zero:
            fw.turn(turn_angle)
            if not drive_is_non_zero:
                drive_time = DRIVE_TIME
                __drive(drive_time=drive_time, drive_forward=True)
            else:
                drive_time = DRIVE_TIME * abs(drive)
                __drive(drive_time=drive_time, drive_forward=(drive > 0))
        elif drive_is_non_zero:
            fw.turn(TURN_ANGLE_CENTER)
            drive_time = DRIVE_TIME * abs(drive)
            __drive(drive_time=drive_time, drive_forward=(drive > 0))
        else:
            drive_time = 0.0

        return json.dumps({
            'status': 'ok',
            'pan_angle': pan_angle,
            'tilt_angle': tilt_angle,
            'turn_angle': turn_angle,
            'drive_time': drive_time,
        }), 200
    except ValueError as e:
        return json.dumps({'status': 'error', 'message': str(e)}), 400
    finally:
        fw.turn(TURN_ANGLE_CENTER)

def __turn_and_drive(turn_angle=120, drive_time=DRIVE_TIME, motor_speed=MOTOR_SPEED, drive_forward=True): 
    fw.turn(turn_angle) 
    __drive(drive_time=drive_time, motor_speed=motor_speed, drive_forward=drive_forward)
    fw.turn(90) 
    pass 

def __look(pan_angle=80, tilt_angle=20): 
    pan_servo.write(pan_angle) 
    tilt_servo.write(tilt_angle) 
    pass 

def __drive(drive_time=DRIVE_TIME, motor_speed=MOTOR_SPEED, drive_forward=True):
    if drive_time <= 0:
        return None
    bw.speed = motor_speed 
    if drive_forward: 
        bw.backward() ## my motors are up-side-down :( 
    else: 
        bw.forward() 
        pass
    sleep(drive_time) ## waint until drive time elapses 
    bw.stop()
    return None

def __read_float_param(name, payload, default=0.0):
    value = request.args.get(name, default=payload.get(name, default))
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f'`{name}` must be a float')

def __validate_range(name, value, low, high):
    if value < low or value > high:
        raise ValueError(f'`{name}` must be in [{low}, {high}]')
    return None

def __map_linear(value, in_min, in_max, out_min, out_max):
    return int(round(out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)))

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000) 
    pass 
