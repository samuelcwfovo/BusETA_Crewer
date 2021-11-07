import hashlib


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
