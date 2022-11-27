import requests 
import json 
import numpy as np 

def img(host): 
    t = __handle_get(f'http://{host}/img') 
    return np.array(json.loads(t)) 

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

