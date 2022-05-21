#!/usr/bin/env python3
import requests
import json
from requests.auth import HTTPBasicAuth


apiKey = 'aebae14aadde49629df26f2f72ed2d57'
params = {'filter[type]': '0,1'}
apiEndpoint = " https://api-v3.mbta.com/routes"
#apiEndpoint = " https://api-v3.mbta.com/routes?filter[type]=0,1"

#8 routes
headers = {"x-api-key" : apiKey}
#auth = HTTPBasicAuth('x-api-key', 'aebae14aadde49629df26f2f72ed2d57')
response = requests.get(apiEndpoint, headers=headers, params=params)

print(json.dumps(response.json(), indent=2))
#print(response.json())
print(response.headers)
print(response.status_code)
print(response.url)

#print (response.json())