import weather_api
api = weather_api.API()

if api.ready == True:
	#Trial storing a temperature
	api.store_reading("temperature", 24.0)
	api.store_reading("temperature", 25.0)
	api.store_reading("temperature", 26.0)
	api.save()
