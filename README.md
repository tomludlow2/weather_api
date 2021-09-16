# weather_api

Weather API Client

## Intro
A Python class (and support files) to link to the weather API so that one can submit weather readings easily
Functions include:
- Easy setup through single registration file with token authentication
- Single line submision of a reading 
- Error commincation back to your script for easy debugging
- Saving ability to sve readings in exportable JSON format for importing into other software

## Setup and Register
1. Ensure that database is setup as per Database file. 
2. Run **register.py**
3. Submit the credential / password for creating a new user on your weather system (setup when installing server side files)
4. Provide the Device Name (e.g. Raspbery Pi), Then Version (e.g. Model 1/3/4), then its Location (e.g. attic, lounge, outside etc)
5. The system will generate an identifier (a key for the readings - useful in case you reinstall later on and want to carry on readings after re-registration)
6. Either accept (N) or create a new identifier (Y)
7. Proceed
8. Test this setup by running  **test_api_setup.py**

## Usage
1. import weather_api
2. create an instance:
3. api = weather_api.API()
4. if api.ready == True: You're ready to go using one of the following files / methods

## Store a reading
- Template File for this:  test_store_reading.py
- import weather_api, create an instance, 
- Then:api.store_reading( paramater, value )
- Then: api.save()
-   This saves the readings to a local file
-   This does not require network access

## Send the readings
- This requires a network connection
- Template File for this: test_send_reading.py


## Acceptable Readings Supported:
- temperature
- humidity
