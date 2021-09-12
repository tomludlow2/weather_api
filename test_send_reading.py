import weather_api
api = weather_api.API()

if api.ready == True:
	#Trial storing a temperature
	api.send_reading("temperature", 24.0)
