#!/usr/bin/env python3
from re import sub
import requests
import json
from requests.auth import HTTPBasicAuth


apiKey = 'aebae14aadde49629df26f2f72ed2d57'
params = {'filter[type]': '0,1'}
apiEndpoint = " https://api-v3.mbta.com/routes"
timeout = 1
#apiEndpoint = " https://api-v3.mbta.com/routes?filter[type]=0,1"

#8 routes
headers = {"x-api-key" : apiKey}
#auth = HTTPBasicAuth('x-api-key', 'aebae14aadde49629df26f2f72ed2d57')
response = requests.get(apiEndpoint, headers=headers, params=params, timeout=timeout)

#print(json.dumps(response.json(), indent=2))
#print(response.json())
#print(response.headers)
#print(response.status_code)
print(response.url)

subwayRouteNames = []
if response.status_code == requests.codes.ok:
    print ("All subway routes fetched successfully.")
    for r in response.json()['data']:
        #debug
        #print(f"Route LongName = {r['attributes']['long_name']}, Description={r['attributes']['description']}")
        subwayRouteNames.append(r['attributes']['long_name'])
print("Subway Routes: ")
print(", ".join(subwayRouteNames))
#print (response.json())