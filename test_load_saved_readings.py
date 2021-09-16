import weather_api
api = weather_api.API()

#Does not require the API to be "ready" - ie network ready
api.read_saved()
