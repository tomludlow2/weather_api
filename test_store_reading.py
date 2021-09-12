import weather_api
api = weather_api.API()

#Does not require the API to be "ready" - ie network ready
api.store_reading("temperature", 24.0)
api.store_reading("temperature", 25.0)
api.store_reading("temperature", 26.0)
api.save()
