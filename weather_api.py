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
		print("INFO: Registration Beginning - please answer these questions to proceed\n")
		c = getpass.getpass("What is the credential for registering a device?: ")
		d = raw_input("What is this device?: ")
		v = raw_input( "What is the device version?: ")
		l = raw_input( "Where is the device located?: ")
		identifier = d + "_" + v + "_" + l;
		identifier = identifier.replace(" ", "_")
		check = "Your device identifier will be: " + identifier + "\n"
		print( check )
		happy = raw_input("Would you like to customise this identifier? (Y/N)  ")
		if( happy == "Y" ):
			identifier = raw_input("Please provide a device identifier: alpha/numeric/-/_ only:  " )
			print( "\nProceeding with custom identifier" )
		elif( happy == "N"):
			print ("\nProceeding with default identifer")
		
		print( "Attempting to register device - please wait...\n")
		dest = self.api_uri + "register.php"
		payload = {
			'credential':c,
			'device_name':d,
			'device_version':v,
			'location':l,
			'identifier':identifier
		}
		req = requests.post(dest, data=payload)
		resp = req.json()
		if resp['registered'] == True:
			print( "Successfully registered account on server - saving config details")
			self.config['device_name'] = d
			self.config['device_version'] = v
			self.config['location'] = l
			self.config['token'] = resp['token']
			self.config['identifier'] = identifier
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

	def save_reading(self, parameter, value):
		#This function saves readings in the internal array
		#This is important in case the device can't connect to the internet
		#Update time to the correct time
		self.update_time()
		reading = {
			'time': self.time,
			'parameter': parameter,
			'reading': value
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
				'identifier':self.config['identifier'],
				'time': self.time,
				'readings': json.dumps(submit)
				}

		
			req = requests.post(dest, data=payload)
			response = req.json()
			if response['insertion_success'] == True:
				if response.get('failed_readings', None) == None:
					print "Success: Reading has been sent to the server"
				else:
					print "Error: Reading could not be saved to the server:"
					print "Info: The accepted variables on the server are:"
					print response['accepted_parameters']
					print "Info: This reading has not been saved locally/remotely - ensure server accepts this reading"
			else:
				print( "Error: While storing data" )
				print(json.dumps(response, indent=4, sort_keys=True))
		else:
			print "Unable to send reading - not ready"

	def send_multiple(self, readings):
		if( self.ready == True):
			#This function is very similar yo send_reading but sends multiple readings (accepts a LIST)
			#Format of list is [ {"temperature":24.0},{"humidity":65.0}] etc
			#Therefore timestamp will  be same on all readings
			#Update time to correct time:
			self.update_time()
			submit = []
			for reading in readings:
				#Create the correct format for submission
				new_reading = {
					'time':self.time
				}
				for key in reading:
					new_reading['parameter'] = key
					new_reading['reading'] = reading[key]
				submit.append(new_reading)
			dest = self.api_uri + "submit_weather.php"
			payload = {
				'token':self.config['token'],
				'identifier':self.config['identifier'],
				'time': self.time,
				'readings': json.dumps(submit)
				}
			print( "Preparing to send multiple readings")
			print(json.dumps(payload, indent=4, sort_keys=False))
			req = requests.post(dest, data=payload)
			response = req.json()
			if response['insertion_success'] == True:
				print( "Success: Readings have been submitted")
			else:
				print( "Error: Readings could not be submitted")
				print( json.dumps(response, indent=4, sort_keys=True))
		else:
			print "Unable to send readings - not ready"


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

	def read_saved(self):
		#Writes out the saved readings pending submission:
		exists = os.path.isfile("saved_readings.json")
		if exists == True:
			f = open( "saved_readings.json", "r")
			readings = json.loads(f.read())
			f.close()
			print( "Readings opened:")
			op = ""
			for r in readings:
				op = op + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r['time']))
				op = op + "- " + r['parameter'] + ": " + str( r['reading']) + "\n"
			print(op)
		else:
			print( "Info: There are no saved readings")

	def send_saved_readings(self):
		#Sends the saved readings to the server and then, if successful, removes them
		exists = os.path.isfile("saved_readings.json")
		if exists == True:
			print("There are files to be sent - attempting to do so")
			f = open( "saved_readings.json", "r")
			readings = json.loads(f.read())
			f.close()
			dest = self.api_uri + "submit_weather.php"
			payload = {
				'token':self.config['token'],
				'identifier':self.config['identifier'],
				'time': self.time,
				'readings': json.dumps(readings)
				}

			req = requests.post(dest, data=payload)
			response = req.json()
			print response
			if response['insertion_success'] == True:
				if response.get('failed_readings', None) == None:
					print "Success: Readings has been sent to the server - removing local file"
					os.remove("saved_readings.json")
				else:
					print "WARNING: Some readings were saved, however there were some that were not."
					print "Info: The accepted variables on the server are:"
					print response['accepted_parameters']
					print "Info: There were some readings that did not match these:"
					print json.dumps(response['failed_readings'], indent=4, sort_keys=True)
					print "The saved_readings file is going to be deleted to prevent duplication"
					os.remove("saved_readings.json")
					conf = raw_input("WARNING: Would you like to save the readings that did not submit? Y/N ")
					if conf == "Y" or conf == "y":
						if os.path.isfile("failed_readings.json") == True:
							print "There are already some failed readings - Merging"
							f = open("failed_readings.json", "r")
							old_readings = json.loads(f.read())
							f.close()
							failed_readings = old_readings + response['failed_readings']
							f = open("failed_readings.json", "w")
							f.write(json.dumps(failed_readings))
							f.close()
							print "Success: Saved Readings to failed_readings.json"
							print "You may wish to input these values manually, or adjust the server to accept these values"
						else:
							print "Creating a failed_readings.json file"
							f = open("failed_readings.json", "w")
							failed_readings = response['failed_readings']
							f.write(json.dumps(failed_readings))
							f.close()
							print "Success: Saved Readings to failed_readings.json"
							print "You may wish to input these values manually, or adjust the server to accept these values"
					else:
						print "OK - these readings have been lost"
				
			else:
				print( "Error While sending data - data has not been deleted" )
				print(json.dumps(response, indent=4, sort_keys=True))
		else:
			print( "Info: There are no saved readings")

	def disablePrint(self):
		sys.stdout = open(os.devnull, "w")

	def enablePrint(self):
		sys.stdout = sys.__stdout__

	def update_time(self):
		self.time = int(time.time())
