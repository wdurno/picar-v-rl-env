# picar-v-rl-env

Apply reinforcement learning toward at-home robotics by manipulating a [PiCar-V](https://github.com/sunfounder/SunFounder_PiCar-V/tree/V3.0). 
- `api_main.py` runs on the PiCar and enables a more-powerful computer to manipulate it with AI software. 
- `car_client.py` runs on the more-powerful server, manipulating the PiCar via the API. 

API dependency: [this](https://github.com/sunfounder/SunFounder_PiCar-V/blob/master/install_dependencies) must be installed on the PiCar. 
It will make the `picar` Python package available. 

Install from local repo (Ubuntu/Debian, modern Python):
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip build
python -m build
python -m pip install dist/car_env-0.0.1-py3-none-any.whl
```

For development (editable install, no wheel build needed):
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Note: On Ubuntu/Debian, `externally-managed-environment` (PEP 668) is expected when installing into system Python. Use a virtual environment as shown above.

More on installs [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/). 
