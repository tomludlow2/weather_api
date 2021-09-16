import weather_api
api = weather_api.API()

if api.ready == True:
	#Trial sending multiple readings
	#Note these will all have the same timestamp on them
	reading_1 = {"temperature": 24.0}
	reading_2 = {"temperature": 26.2}
	reading_3 = {"temperature": 28.1}
	reading_4 = {"humidity": 58}
	reading_5 = {"humidity": 60}
	reading_6 = {"humidity": 64}

	readings = [reading_1, reading_2, reading_3, reading_4, reading_5, reading_6]
	api.send_multiple(readings)
