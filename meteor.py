import requests
import math

# function to calculate distance between to locations expresed in long and lat
def calc_dist(lat1, lon1, lat2, lon2):
  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)
  h = math.sin( (lat2 - lat1) / 2 ) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin( (lon2 - lon1) / 2 ) ** 2
  return 6372.8 * 2 * math.asin(math.sqrt(h))

# function that returns the dist value from a list, and if that is empty retun infinity
def get_dist(m):
  return m.get('dist', math.inf)

# set my location, hardcoded for now
my_location_latitude = 43.70801618350077
my_location_longitude = -79.38968539237976

# call NASA API for meteor strikes
meteor = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
# check if the request was ok
if meteor.status_code != 200:
  print('something went wrong with the request to NASA API, exiting')
  exit()
# format the returned data in JSON 
m_data = meteor.json()

# add dist[ance] to the each element of the dict if it has the long and lat of the hit
for hit in m_data:
  if 'reclong' not in hit or 'reclat' not in hit: continue
  hit_long = float(hit['reclong'])
  hit_lat = float(hit['reclat'])
  hit['dist'] = calc_dist(my_location_latitude,my_location_longitude,hit_lat,hit_long)
  # print('This hit was at long: {0} and lat: {1}'.format(hit_long,hit_lat)) # debug print statment 

# sort the dict accorting to the value in the dist field we just added
# notice this is done by passing a function as the sort key 
m_data.sort(key=get_dist)

# print 3 closest location of meteor hits
for closeby in m_data[0:3]:
  print('A meteor hit on {0} at {1} that''s {2} km away from me'.format(closeby['year'],closeby['name'],closeby['dist']))

# what does this do?
# m_data[-1:-11:-1]

# number of records in the dict that do not have dist record
# len([m for m in m_data if 'dist' not in m])