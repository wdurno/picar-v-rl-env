import requests 
import json 
import numpy as np 
import random 
from time import time, sleep 
from car import BALL_SIZE_MIN, BALL_SIZE_MAX, find_blob 

## CONSTANTS 
N_ACTIONS = 8 

## CLIENT 

def img(host): 
    t = __handle_get(f'http://{host}/img') 
    return np.array(json.loads(t)).astype(np.uint8)  

def drive_left(host): 
    __handle_get(f'http://{host}/drive-left') 
    pass 

def drive_right(host): 
    __handle_get(f'http://{host}/drive-right') 
    pass 

def drive_forward(host): 
    __handle_get(f'http://{host}/drive-forward') 
    pass 

def drive_backward(host): 
    __handle_get(f'http://{host}/drive-backward') 
    pass 

def look_left(host): 
    __handle_get(f'http://{host}/look-left') 
    pass 

def look_right(host): 
    __handle_get(f'http://{host}/look-right') 
    pass 

def look_up(host): 
    __handle_get(f'http://{host}/look-up') 
    pass 

def look_forward(host): 
    __handle_get(f'http://{host}/look-forward') 
    pass 

def __handle_get(url): 
    r = requests.get(url) 
    if r.status_code != 200: 
        raise Exception(f'ERROR! Status code: {r.status_code}') 
    return r.text 

## RL ENV 

class PiCarEnv(): 
    def __init__(self, host): 
        self.host = host 
        look_forward(self.host) 
        self.camera = 0 
        self.last_image = img(self.host) 
        self.last_action_time = time() 
        pass 
    def reset(self): 
        look_forward(self.host) 
        self.camera = 0 
        return img(self.host), self.camera  
    def action_space_sample(self): 
        return random.randint(0, N_ACTIONS-1) ## sampling range is inclusive 
    def step(self, action): 
        if action in PiCarEnv.__action_dict: 
            PiCarEnv.__action_dict[action](self.host) 
            pass ## implicit else: no-op 
        if action in PiCarEnv.__look_dict: 
            self.camera = PiCarEnv.__look_dict[action] 
            pass 
        image = img(self.host) 
        self.last_image = image 
        self.last_action_time = time() 
        return image, self.camera 
    def auto_action(self): 
        t = time()
        if t - self.last_action_time < .1: 
            ## avoid overheats 
            sleep(.1 - t + self.last_action_time) 
            pass 
        (x, y), r = find_blob(self.last_image) 
        action = self.suggest_action(x, r) 
        self.step(action) 
        pass 
    def suggest_action(self, ball_x_location, ball_radius): 
        left = 20 
        center = 30 
        right = 40 
        if ball_radius == 0: 
            ## no ball seen 
            ## scan for it 
            if self.camera == 0:
                return 4 ## look_right 
            elif self.camera == 1: 
                return 6 ## look_up 
            elif self.camera == 3: 
                return 5 ## look_right 
            else: 
                return 7 ## look_forward 
        elif self.camera == 1: 
            ## looking left 
            if ball_x_location < center: 
                ## drive left, toward it 
                return 0 ## drive_left 
            else: 
                ## center the camera 
                return 7 ## look_forward 
        elif self.camera == 2: 
            ## looking right 
            if ball_x_location > center: 
                ## drive right, toward it 
                return 1 ## drive_right 
            else: 
                ## center the camera 
                return 7 ## look foward 
        else: 
            ## camera is foward or up 
            if ball_x_location < left: 
                ## drive left, toward it 
                return 0 ## drive_left 
            elif ball_x_location > right: 
                return 1 ## drive_right 
            else: 
                ## ball is center 
                if ball_radius < BALL_SIZE_MAX: 
                    return 2 ## drive_forward 
                else: 
                    return 3 ## drive_backward 
        pass 
    @staticmethod 
    def get_reward(ball_radius): 
        ## reward being close to the ball 
        if ball_radius >= BALL_SIZE_MIN and ball_radius <= BALL_SIZE_MAX: 
            return(ball_radius - BALL_SIZE_MIN ) / (BALL_SIZE_MAX - BALL_SIZE_MIN) 
        elif ball_radius > BALL_SIZE_MAX: 
            ## slight punishment for being too close 
            return min(1. + (BALL_SIZE_MAX - ball_radius)/20., -.1) 
            pass 
        return 0.  
    __action_dict = { 
            0: drive_left, 
            1: drive_right, 
            2: drive_forward, 
            3: drive_backward, 
            4: look_left, 
            5: look_right, 
            6: look_up, 
            7: look_forward 
            } 
    __look_dict = { ## map action ints to camera state ints 
            4: 1, ## left 
            5: 2, ## right 
            6: 3, ## up 
            7: 0  ## foward 
            } 
    pass 
