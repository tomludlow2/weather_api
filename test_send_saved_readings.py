import weather_api
api = weather_api.API()

if api.ready == True:
	#Trial sending all the saved readings
	api.send_saved_readings()
