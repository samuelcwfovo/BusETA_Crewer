import json
import requests


kmb_route_file = open('kmbRoute.json','rb')

kmb_route_data = json.load(kmb_route_file)
kmb_route_file.close()

kmb_route_dict = {}
for kmb_route in kmb_route_data['data']:
    if kmb_route['route'] in kmb_route_dict:
        kmb_route_dict[kmb_route['route']] += 1
    else:
        kmb_route_dict[kmb_route['route']] = 1



download_route_file = open('routes.json','rb')
download_route_data = json.load(download_route_file)
download_route_file.close()


#hotFix
download_route_data.pop('7152', None)
download_route_data.pop('7439', None)
download_route_data.pop('5020', None) #115P


#check is route stop list valid
should_remove_route_dict = []
for key, route in download_route_data.items():
    if 'route' in route:
        if len(route['route']) == 0 :
            should_remove_route_dict.append(key)

for key in should_remove_route_dict:
    download_route_data.pop(key, None)


download_route_dict = {}
for key, route in download_route_data.items():
        if "LWB" in route['company']['code'] or "KMB" in route['company']['code']:
                if route['routeName_en_us'] in download_route_dict:
                    download_route_dict[route['routeName_en_us']] += 1
                else:
                    download_route_dict[route['routeName_en_us']] = 1



# remove outdated route
should_remove_dict_key = []
for route, count in download_route_dict.items():
    if route not in kmb_route_dict:
        should_remove_dict_key.append(route)
        should_remove_key = []
        for key, value in download_route_data.items():
            if value['routeName_en_us'] == route:
                should_remove_key.append(key)
        
        for key in should_remove_key:
            download_route_data.pop(key, None)

for key in should_remove_dict_key:
    download_route_dict.pop(key, None)


#
for route, count in download_route_dict.items():
    if count > kmb_route_dict[route]:
        print(route, " kmb count: ", kmb_route_dict[route], " download count: ", count)

# print(download_route_dict)



with open('routes_final.json', 'w', encoding='utf-8') as f:
    json.dump(download_route_data, f, ensure_ascii=False)


