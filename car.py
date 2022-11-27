## this is basically just ball_tracker.py (linked), reduced to an API 
## link: https://github.com/sunfounder/SunFounder_PiCar-V/blob/V3.0/ball_track/ball_tracker.py 
## 
## primary interface: 
## - img ## img.read(), img.release() 
## - find_blob() ## returns (x, y), radius 
## - fw ## front wheels, ie. fw.turn(90)  
## - bw ## back wheels, ie. bw.speed = 60, bw.stop(), bw.forward() 


from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

picar.setup()
# Show image captured by camera, True to turn on, you will need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

if (show_image_enable or draw_circle_enable) and "DISPLAY" not in os.environ:
    print('Warning: Display not found, turn off "show_image_enable" and "draw_circle_enable"')
    show_image_enable   = False
    draw_circle_enable  = False

kernel = np.ones((5,5),np.uint8)
img = cv2.VideoCapture(-1)

if not img.isOpened:
    print("not open")
else:
    print("open")
    
SCREEN_WIDTH = 80 ## reduced by half for more-efficient AI processing 
SCREEN_HIGHT = 60 ## also reduced by half 
img.set(3,SCREEN_WIDTH)
img.set(4,SCREEN_HIGHT)
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
BALL_SIZE_MIN = SCREEN_HIGHT/10
BALL_SIZE_MAX = SCREEN_HIGHT/3

# Filter setting, DONOT CHANGE
hmn = 12
hmx = 37
smn = 96
smx = 255
vmn = 186
vmx = 255

CAMERA_STEP = 2
CAMERA_X_ANGLE = 20
CAMERA_Y_ANGLE = 20

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

SCAN_POS = [[20, TILT_ANGLE_MIN], [50, TILT_ANGLE_MIN], [90, TILT_ANGLE_MIN], [130, TILT_ANGLE_MIN], [160, TILT_ANGLE_MIN],
            [160, 80], [130, 80], [90, 80], [50, 80], [20, 80]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
pan_servo.offset = 10
tilt_servo.offset = 0

bw.speed = 0
fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)

motor_speed = 60

def nothing(x):
    pass

def destroy():
    bw.stop()
    img.release()

def test():
    fw.turn(90)

