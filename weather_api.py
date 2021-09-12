import requests, time, getpass, json, os, sys

class API:
	api_uri = "https://api.tomludlow.co.uk/"
	config = {
		'token':0
	}
	ready = False
	time = int(time.time())
	readings = []

	def __init__(self, quiet=False):
		#Quiet mode prevents output (mainly for registering)
		if quiet == True:
			self.disablePrint()
		print("Initialising API")
		if os.path.isfile("api_config.json") == True:
			print ("Loading API Configuration" )
			f = open("api_config.json", "r")
			self.config = json.loads(f.read())
			f.close()
			print ("Config Loaded")

			dest = self.api_uri + "status.php"
			payload = {
				'time': self.time,
				'token': self.config['token']
			}
			req = requests.post(dest, data=payload)
			resp = req.json()
			if resp['token_valid'] == True and resp['system_live'] == True and resp['connected'] == True and resp['db_live'] == True and resp['token_present'] == True and resp['token_query'] == True:
				print("Success: Token loaded and checked - ready to proceed")
				self.ready = True
			else:
				print("Error: Token loaded and checked - NOT ready to proceed")
				print("Checking for errors:")
				if resp['token_valid'] == True:
					print( "Test: Check API Token validity: SUCCESS - PASS")
				else:
					print( "Test: Check API Token validity: ERROR - FAIL")
					print( "Info: API token is invalid - re-register")
				if resp['system_live'] == True:
					print( "Test: System Live: SUCCESS - PASS")
				else:
					print( "Test: System Live: ERROR - FAIL")
					print( "Info: System has been turned off, this is not an error in the client")
				if resp['connected'] == True:
					print( "Test: Connected: SUCCESS - PASS")
				else:
					print( "Test: Connected: ERROR - FAIL")					
					print( "Info: This only fails when PHP throws an error / json is not encoded")
				if resp['db_live'] == True:
					print( "Test: Remote Database: SUCCESS - PASS")
				else:
					print( "Test: Remote Database: ERROR - FAIL")					
					print( "Info: Server connection error - server conn file may be corrupt")
				if resp['token_present'] == True:
					print( "Test: Token Received: SUCCESS - PASS")
				else:
					print( "Test: Token Received: ERROR - FAIL")					
					print( "Info: The token was not received by the server")
				if resp['token_query'] == True:
					print( "Test: Token Query: SUCCESS - PASS")
				else:
					print( "Test: Token Query: ERROR - FAIL")					
					print( "Info: The system is running, but the token that was sent resulted in a failing SQL Query")

		else:
			print("Info: API Not Setup - no Config File")
		self.enablePrint()
		return

	def register(self):
		d = raw_input("What is this device?: ")
		v = raw_input( "What is the device version?: ")
		l = raw_input( "Where is the device located?: ")
		c = getpass.getpass("What is the credential for registering a device?: ")
		print( "Attempting to register device - please wait...")
		dest = self.api_uri + "register.php"
		payload = {
			'credential':c,
			'device_name':d,
			'device_version':v,
			'location':l
		}
		req = requests.post(dest, data=payload)
		resp = req.json()
		if resp['registered'] == True:
			print( "Successfully registered account on server - saving config details")
			self.config['device_name'] = d
			self.config['device_version'] = v
			self.config['location'] = l
			self.config['token'] = resp['token']
			#Check if a config file exists
			exists = os.path.isfile("api_config.json")
			if exists == True:
				print( "Info: Config file already exists - overwriting with new registration")
				f = open("api_config.json", "w")
				f.write(json.dumps(self.config))
				f.close()
				print ("Success: Config file re-created")
			else:
				print( "Info: Creating first config file")
				f = open("api_config.json", "w")
				f.write(json.dumps(self.config))
				f.close()
				print ("Success: API has been registered, and config details have been stored")
		else:
			print("Error: Could not register user")
			print(req.text)

	def store_reading(self, parameter, value):
		#This function stores readings in the internal array
		#This is important in case the device can't connect to the internet
		#Update time to the correct time
		self.update_time()
		reading = {
			'time': self.time,
			'parameter': parameter,
			'reading:': value
		}
		self.readings.append(reading)
		op = "Stored a new " + parameter + ", value: " + str(value)
		print op

	def send_reading(self, parameter, value):
		if( self.ready == True ):
			#This function sends a single reading
			#Update time to the correct time
			self.update_time()
			reading = {
				'time': self.time,
				'parameter': parameter,
				'reading': value
			}
			submit = []
			submit.append(reading)

			dest = self.api_uri + "submit_weather.php"
			payload = {
				'token':self.config['token'],
				'time': self.time,
				'readings': json.dumps(submit)
				}

		
			req = requests.post(dest, data=payload)
			response = req.json()
			print(json.dumps(response, indent=4, sort_keys=True))
		else:
			print "Unable to send reading - not ready"

	def save(self):
		#Save any store readings as in a save file:
		exists = os.path.isfile("saved_readings.json")
		if exists == True:
			print "There are already some saved readings - Merging"
			f = open("saved_readings.json", "r")
			old_readings = json.loads(f.read())
			f.close()
			self.readings = old_readings + self.readings
			f = open("saved_readings.json", "w")
			f.write(json.dumps(self.readings))
			f.close()
			print "Success: Saved Readings to saved_readings.json"
		else:
			print "Saving Readings to new file"
			f = open("saved_readings.json", "w")
			f.write(json.dumps(self.readings))
			f.close()
			print "Success: Saved Readings to saved_readings.json"

	def disablePrint(self):
		sys.stdout = open(os.devnull, "w")

	def enablePrint(self):
		sys.stdout = sys.__stdout__

	def update_time(self):
		self.time = int(time.time())
