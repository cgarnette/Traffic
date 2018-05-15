import json
import os
from datetime import date
from datetime import datetime

import requests
import math

class Traffic(object):

	dir_path = os.path.dirname(os.path.realpath(__file__))

##I Want this to output the severity, type, and location of an incident

##I will give a certain area. I want it to check that area for any incidents (2, 4).
######the purpose of this is just to see if normal conditions are affecting Uber prices

#Next I will give it the entire DC area and check for incidents (2, 4, 7, 11)
######Same purpose as above, but less specific to certain areas. I will want to save the locations of these incidents

#Also document severity just in case.


#Meanings of Traffic Incident Numbers:
#1. Accident
#2. Congestion
#3. Disabled Vehicle
#4. Mass Transit
#5. Misc.
#6. Other News
#7. Planned Event
#8. Road Hazard
#9. Construction
#10. Alert
#11. Weather

#Meanings of Severity Numbers:
#1. Low Impact
#2. Minor
#3. Moderate
#4. Serious

	def getLongitude(self, cLong):
		var = math.cos(math.radians(cLong)) * 69.2 #one degree of longitude equals this many miles
		var = 1/var
		return var

	def getIncidents(self, coordinates):
		#half a mile in latitude = .007 degrees
		southLat = coordinates[0] - .014 #(.007)
		northLat = coordinates[0] + .014 #(.007)

		longInterval = self.getLongitude(coordinates[1])

		eastLong = coordinates[1] + (longInterval)
		westLong = coordinates[1] - (longInterval)

		#print('South:' + str(southLat) + '\nNorth:' + str(northLat) + '\nEastLong:' + str(eastLong) + '\nWestLong:' + str(westLong))
		if (not os.path.exists(self.dir_path + '\\Log')):
			os.makedirs(self.dir_path + '\\Log')
		
		log = open(self.dir_path + '\\Log\\Log.txt', 'w+')

		try:
			resp = requests.get('http://dev.virtualearth.net/REST/v1/Traffic/Incidents/{:.6f},{:.6f},{:.6f},{:.6f}?t=1,2,4,7,9,11&key='.format(southLat,westLong,northLat,eastLong)+self.key)
		except:
			print('There was an error connecting to the Bing Maps Api Server. \nCheck network settings or address input')
			log.write('There was an error connecting to Bing Maps Api :::' + str(datetime.now()) + '\n')
			log.close()
			return None
			
		log.close()
		reportNum = json.loads(resp.text)['resourceSets'][0]['estimatedTotal']

		i = 0

		reports = {}
		for item in json.loads(resp.text)['resourceSets'][0]['resources']:#[i]:
			
			reports[str(i)] = {'Type': str(item['type']), 'Severity': str(item['severity'])}
			i = i + 1

		return reports

	def getTravelTime(self, start, end):

		if (not os.path.exists(self.dir_path + '\\Log')):
			os.makedirs(self.dir_path + '\\Log')

		log = open(self.dir_path + '\\Log\\Log.txt', 'w+')

		if(self.googleKey is None):
			print('You must use a Google Maps Api Key')
			log.write('No Google Maps Api Key present:::' + str(datetime.now()) + '\n')
			log.close()
			return None
		try:
			resp = requests.get('https://maps.googleapis.com/maps/api/directions/json?&mode=driving&origin='+start['street']+','+start['city']+','+start['state']+'&destination='+end['street']+','+end['city']+','+end['state']+'&key='+self.googleKey)
		except:
			print('There was an error connecting to the Google Maps Api Server. \nCheck network settings or address input')
			log.write('There was an error connecting to Google Maps Api :::' + str(datetime.now()) + '\n')
			log.close()
			return None
		
		report = json.loads(resp.text)
		travelTime = int(report['routes'][0]['legs'][0]['duration']['value']/60)

		return travelTime


	def getAddress(self, state, city, street):

		fullSt = ''

		parts = street.split(' ')

		if (not os.path.exists(self.dir_path + '\\Log')):
			os.makedirs(self.dir_path + '\\Log')

		log = open(self.dir_path + '\\Log\\Log.txt', 'w+')

		i = 0
		for partial in parts:
			if(i < 1):
				fullSt = partial
			else:
				fullSt = fullSt + '%20' + partial
			i += 1

		if(self.key is None):
			print('You must use a Bing Maps Api Key')
			log.write('No Bing Maps Api Key present:::' + str(datetime.now()) + '\n')
			log.close()
			return None
		try:
			resp = requests.get('http://dev.virtualearth.net/REST/v1/Locations/US/'+state+'/'+city+'/'+fullSt+'?output=json&key='+str(self.key))
			coordinates = json.loads(resp.text)['resourceSets'][0]['resources'][0]['point']['coordinates']
			log.close()
			return coordinates
		except:
			print('There was an error connecting to the Bing Maps Api Server. \nCheck network settings or address input')
			log.write('There was an error connecting to Bing Maps Api :::' + str(datetime.now()) + '\n')
			log.close()
			return None

	
	def __init__(self, key=None, googleKey=None):
		self.key = key
		self.googleKey = googleKey



#key = 'AiM0oSivEbqBK4wxK_qCeFPqn0Y5PCdiTwjsdAXKBaq-VHBeRzpcuPIJogLFXwJB'
#t = Traffic(key)

#state = 'DC'
#street = '1111 Constitution Ave NW' #'1940 9th St NW'
#city = 'Washington'

#coord = t.getAddress(state, city, street)

#report = t.getIncidents(coord)

#i=0
#while(i < len(report)):
#	print(report[str(i)])
#	i += 1


# store file with coordinates, time(military), type of incident, severity, day of week, date
# for uber store either coordinates or address, time(military), cost x, cost pool, cost xl, day of week, date