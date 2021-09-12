import weather_api

print( "Testing the API Setup" )
print( "Loading API Module" )
api = weather_api.API(False)

print( "Checking if API is ready" )
if api.ready == True:
	print("Success: API has loaded")
else:
	print( "Error: API has loaded but is not ready to be used" )
