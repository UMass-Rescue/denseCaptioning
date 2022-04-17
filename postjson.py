import requests
import json

f = open('/home/chaoticmonkey/Desktop/Rescue/DenseCap/densecap/vis/data/results.json')
data = json.load(f)
r = requests.post('http://0.0.0.0:8080/', json=data)
print(r.status_code)
print(r.json())
