#!/usr/bin/env python3
import requests
import json
import networkx as nx
import sys
import getopt
import traceback

from util.bc_utility import *

def main(argv):
    G = nx.Graph()


    apiKey = 'aebae14aadde49629df26f2f72ed2d57'
    #filter by type 0 and 1 which is light rail and heavy rail respectively
    params = {'filter[type]': '0,1', 'fields[route]': 'long_name,id'}
    routesEndpoint = " https://api-v3.mbta.com/routes"
    #https://api-v3.mbta.com/stops?include=route&filter%5Broute%5D=Red
    timeout = 180
    #apiEndpoint = " https://api-v3.mbta.com/routes?filr[type]=0,1"

    #8 routes
    headers = {"x-api-key" : apiKey}
    routesResp = requests.get(routesEndpoint, headers=headers, params=params, timeout=timeout)

    #print(json.dumps(response.json(), indent=2))
    #print(response.json())
    #print(response.headers)
    #print(response.status_code)
    print(routesResp.url)

    subwayRouteNames = {}
    if routesResp.status_code == requests.codes.ok:
        print ("All subway routes fetched successfully.")
        for r in routesResp.json()['data']:
            #debug
            print(f"Route LongName = {r['attributes']['long_name']}, ID={r['id']}")
            subwayRouteNames[r['id']] = r['attributes']['long_name']
            #subwayRouteNames.append(r['attributes']['long_name'])
    print("Subway Routes: ")
    print(", ".join(subwayRouteNames.values()))
    #print (response.json())

    stopsEndpoint = " https://api-v3.mbta.com/stops"
    #https://api-v3.mbta.com/stops?include=route&filter%5Broute%5D=Red #sample api call
    for routeId in subwayRouteNames:
        params = {'filter[route]': routeId, 'include': 'route', 'fields[stops]': 'name'}
        stopsResp = requests.get(stopsEndpoint, headers=headers, params=params, timeout=timeout)
        if stopsResp.status_code == requests.codes.ok:
            print (f"All stops routes fetched successfully for route {subwayRouteNames[routeId]}.")
            for sr in stopsResp.json()['data']:
                 print(f"Stop Name= {sr['attributes']['name']}, ID={sr['id']}")

        #print (stopsResp.json())

#utility method for exception handling
def exitWithException(eCode):
    try:
        raise BCException(eCode)
    except BCException as e1:
        print("Error code: %s" % e1.code)
        BCUtility.printError(e1.message)
        #traceback.print_exc()
        sys.exit(eCode)

#prints usage help
def printUsageHelp(eCode):
    print (eCode)
    print ("python3 compass.py -e <entsoFile:string> -g <gppdFile:string> -p <plattsFile:string> -n <normalizePlantNames:bool> -v")
    print ("\t-h = Usage help")
    print ("\t-e or --entsoFile = (OPTIONAL) Path to the CSV file with ENTSO data. Default (if unset): entso.csv in data directory")
    print ("\t-g or --gppdFile = (OPTIONAL) Path to the CSV file with GPPD data. Default (if unset): gppd.csv in data directory")
    print ("\t-p or --plattsFile = (OPTIONAL) Path to the CSV file with Platts data. Default (if unset): platts.csv in data directory")
    print ("\t-n or --normalizePlantNames = (OPTIONAL) Whether or not to perform names normalization based on plant_names in ENTSO file (this tend to increase runtime but more matches can be found). Default (if unset): True")
    print ("\t-v or --verbose = (OPTIONAL) Print the status of TL execution in more detail.")
    if eCode == ReturnCodes.SUCCESS:
        sys.exit(eCode)
    try:
        raise BCException(eCode)
    except BCException as e1:
        print (e1.message)
        traceback.print_exc()
        sys.exit(eCode)
        
if __name__ == "__main__":
	main(sys.argv[1:])
