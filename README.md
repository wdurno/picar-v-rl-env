# picar-v-rl-env

Apply reinforcement learning toward at-home robotics by manipulating a [PiCar-V](https://github.com/sunfounder/SunFounder_PiCar-V/tree/V3.0). 
- `api_main.py` runs on the PiCar and enables a more-powerful computer to manipulate it with AI software. 
- `car_client.py` runs on the more-powerful server, manipulating the PiCar via the API. 

API dependency: [this](https://github.com/sunfounder/SunFounder_PiCar-V/blob/master/install_dependencies) must be installed on the PiCar. 
It will make the `picar` Python package available. 

Install from local repo:
```
python3 -m pip install --upgrade build
python3 -m build 
pip3 install dist/car_env-0.0.1-py3-none-any.whl  
```

More on installs [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/). 

