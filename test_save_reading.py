import weather_api
api = weather_api.API()

#Does not require the API to be "ready" - ie network ready
api.save_reading("temperature", 24.0)
api.save_reading("humidity", 28.0)
api.save_reading("failed_reading", 26.0)
api.save_reading("failed_reading_2", 68.0)
api.save()
