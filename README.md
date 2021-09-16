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

## Save a reading
- Template File for this:  **test_save_reading.py**
- import weather_api, create an instance, 
- Then:api.save_reading( paramater, value )
- Then: api.save()
-   This saves the readings to a local file
-   This does not require network access

#### Load a reading
- Template File for this: **test_load_saved_readings.py**
- This will load and print out the saved readings

## Send Readings
- This requires a network connection

#### Send a single reading
- Template File for this: **test_send_reading.py**
- Very simple mechanism to just send one reading
- Just pass (paramater, reading) and it will send

#### Send mutiple readings:
- Template File for this:  **test_send_multiple.py**
- This is for sending multiple readings together (will have the same timestamp
- Anticipate usage will be for taking e.g. Temperature + Humidity at the same time and then send them together
- Not for, for example, storing multiple readings over time and then send them together as their timestamps will not be sent correctly

#### Send saved readings:
- Template File for this: **test_send_saved_readings.py**
- This will open the saved_readings.json file, load in the readings, and then attempt to send them
- This will either lead to Success - in which case they have all been sent
- Or it will lead to failure either due to a server issue OR
- If you have saved a parameter that your server is not configured to accept, it will let you know
- It will then offer you the option of saving the "failed readings" into a new json file for later manipulation
- If you choose not to do this, the failed readings will be lost.

## Acceptable Readings Supported:
- temperature
- humidity
