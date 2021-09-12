import  weather_api

print "Welcome to the registration system"
print "Please fill in the following fields to register a device"

api = weather_api.API(True)
api.register()
