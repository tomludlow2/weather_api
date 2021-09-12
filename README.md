# weather_api

Weather API Client

# Intro
A Python class (and support files) to link to the weather API so that one can submit weather readings easily

# Setup
1. Run register.py
2. Submit the information requested e.g. "Raspberry Pi",  "Model 3", "Attic"
3. The credential facilitates the addition to the system - this is created in the server-side file receiving your api calls
4. Test this with test_api_setup.py

# Usage
1. import weather_api
2. create an instance:
3. api = weather_api.API()
4. if api.ready == Tre: You're ready to go using one of the following files
