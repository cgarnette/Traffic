# Traffic

This is a small project done to demonstrate and simplify the usage of both the Bing Maps API and Google Maps API integrated with python.

## Prerequisites

1. requests

## Installation

Download TrafficInfo.py

pip install requests

## Getting Started

This class is used to get traffic information from both Bing Maps and Google Maps API servers.

Use the following script to get started. (mapsKey is Bing Maps API key)

```
# This will return a tuple with the latitude and longitude for the address passed as a parameter.

# mapsKey=''
# googleAPiKey=''
#state = ''
#city = ''
#street = ''

t = Traffic(mapsKey, googleApiKey)
coords = t.getAddress(state, city, street)

# This will return a dictionary with a nested dictionary. i.e. {Key: {Key: Value, Key: Value}} where the outer key is the incident number and the inner keys are either "Type" or "Severity".

startIncidents = t.getIncidents(coords)

# This following portion will convert the address into a format that can be understood by the Google Maps API.

def googlePrep(x):
	parts = x.split(' ')
	full = ''
	i = 0
	for partial in parts:
		if(i < 1):
			full = partial
		else:
			full = full + '+' + partial
		i += 1
	return full
  
  # You can then proceed to use Google Maps to calculate travel time by using the following:
  
  startDict = {'state':state, 'street': googlePrep(street), 'city':googlePrep(city)} # This is your starting address
  endDict = {'state':state, 'street': googlePrep(street), 'city':googlePrep(city)}  # This is your destination address
  
  travelTime = t.getTravelTime(startDict, endDict)
  
  # travelTime will be an integer estimation of the travel time between the two points, calculated in minutes.
```
