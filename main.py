
import requests
import json
import hashlib

stop_url = 'https://storage.googleapis.com/linkingplatform.appspot.com/cache/stopV3.json'
route_url = 'https://storage.googleapis.com/linkingplatform.appspot.com/cache/routeV3.json'

stops = requests.get(stop_url).json()
routes = requests.get(route_url).json()

final_routes = {}

for stop in stops:
    for route_stop in stop["routeStops"]:
        found = False
        for route in routes:
            if route['sId'] == route_stop['routeID'] and route['bounding'] == route_stop['bounding']:
                route_stop['route_unique_ID'] = route['id']
                found = True
                break
        if not found:
            # route_data not found in route_stop list
            # thats mean some route_stop data error.
            pass
            
for route in routes:
    final_routes[route['id']] = route



#output file
with open('routes.json', 'w', encoding='utf-8') as f:
    json.dump(final_routes, f, ensure_ascii=False)

with open('stops.json', 'w', encoding='utf-8') as f:
    json.dump(stops, f, ensure_ascii=False)


#md5
with open("routes.json", "rb") as f:
    routes_hash = hashlib.md5()
    while chunk := f.read(8192):
        routes_hash.update(chunk)

with open('routes.md5', 'w', encoding='utf-8') as f:
    f.write(routes_hash.hexdigest())


with open("stops.json", "rb") as f:
    stops_hash = hashlib.md5()
    while chunk := f.read(8192):
        stops_hash.update(chunk)

with open('stops.md5', 'w', encoding='utf-8') as f:
    f.write(stops_hash.hexdigest())
