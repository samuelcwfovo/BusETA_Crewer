
import requests
import json
import asyncio

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


# get routes stops data
loop = asyncio.get_event_loop()
process = []
tasks = []

async def check_route_api(sid, bounding, id, p, r):
    url = "https://api.linkingapp.com/HKBussez/v3/route/{}/{}".format(sid, bounding)
    res = await loop.run_in_executor(None,requests.get,url)
    p.append(id)
    print(" check point: {} / {}".format(len(p), len(tasks)))

    json_data = res.json()
    if len(json_data) > 1 :
        print(" >1 : ", id)
    r[id] = json_data[0]

for key, route in final_routes.items():
    if "LWB" in route['company']['code'] or "KMB" in route['company']['code'] or "NLB" in route['company']['code'] or "CTB" in route['company']['code']:
        task = loop.create_task(check_route_api(route['sId'], route['bounding'], route['id'], process, final_routes))
        tasks.append(task)

#test
# task = loop.create_task(check_route_api(1468, 1, 5734, process, final_routes))
# tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))



#output file
with open('routes.json', 'w', encoding='utf-8') as f:
    json.dump(final_routes, f, ensure_ascii=False)

with open('stops.json', 'w', encoding='utf-8') as f:
    json.dump(stops, f, ensure_ascii=False)

