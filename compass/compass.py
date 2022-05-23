#!/usr/bin/env python3
'''
	This is the main module for Boston-compass. This covers all my solution to Broad's coding questions.
    
    @author Kevin Palis <kevin.palis@gmail.com>
'''

import requests
import json
import networkx as nx
import sys
import getopt
import traceback

from util.bc_utility import *

def main(argv):
    isVerbose = True

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

    #The solution to question #1: Print all long_names of all routes of type 0 and 1, ie. subway routes
    #I'm using the filtering on the server-side here, ie. as parameter to the API call. This is better because it avoids unnecessary passing of data that can saturate the network and make everything slower
    # It also makes more sense to do the filtering in the server because typically, we don't really know the data model in the actual database storage. The API will know how to optimize filtering, to the point
    # that it can take advantage of actual SQL (in the case of RDBMS) or any advanced filtering/caching (in the case of noSQL storage solutions). But as a client script, we don't need to worry about any of 
    # # that as the web service handles all those for us.
    subwayRouteNames = {}
    if routesResp.status_code == requests.codes.ok:
        for r in routesResp.json()['data']:
            #debug
            #print(f"Route LongName = {r['attributes']['long_name']}, ID={r['id']}")
            subwayRouteNames[r['id']] = r['attributes']['long_name']
    print("\nAll Subway Routes: ")
    print(", ".join(subwayRouteNames.values()))
    #print (response.json())

    #The solution to question #2. There are a few requirements here, namely, print:
    # 1. The name of the subway route with the most stops as well as a count of its stops.
    # 2. The name of the subway route with the fewest stops as well as a count of its stops.
    # 3. A list of the stops that connect two or more subway routes along with the relevant route names for each of those stops. 
    stopsEndpoint = " https://api-v3.mbta.com/stops"
    #https://api-v3.mbta.com/stops?include=route&filter%5Broute%5D=Red #sample api call
    subwayStopsCount = {}
    stops = {} #dictionary of all the stops with the routes that stop at them as values
    #graph to store stops as vertices/nodes
    bostonSubway = nx.Graph()
    prevNode = None
    #for each route, get all the stops
    for routeId in subwayRouteNames:
        params = {'filter[route]': routeId, 'include': 'route', 'fields[stops]': 'name'}
        stopsResp = requests.get(stopsEndpoint, headers=headers, params=params, timeout=timeout)
        if stopsResp.status_code == requests.codes.ok:
            #debug
            #print (f"All stops routes fetched successfully for route {subwayRouteNames[routeId]}.")
            subwayStopsCount[subwayRouteNames[routeId]] = 0
            for sr in stopsResp.json()['data']:
                #print(f"Stop Name= {sr['attributes']['name']}, ID={sr['id']}")
                subwayStopsCount[subwayRouteNames[routeId]]+=1
                stops = upsertValuesToDict(stops, sr['attributes']['name'], [subwayRouteNames[routeId]])
                if prevNode is not None:
                    #debug - prints all edges as they are being added:
                    #print (f"Adding edge from {prevNode} to {sr['attributes']['name']} with attribute {subwayRouteNames[routeId]}")
                    bostonSubway.add_edge(prevNode, sr['attributes']['name'], route=subwayRouteNames[routeId])
                prevNode = sr['attributes']['name']
            prevNode = None

    if isVerbose:
        print (f"\nTally of all the routes' stops: {subwayStopsCount}")
    maxStopsRoute = max(subwayStopsCount, key=subwayStopsCount.get)
    print (f"\nRoute with the most stops: {maxStopsRoute} has {subwayStopsCount[maxStopsRoute]} stops.")
    minStopsRoute = min(subwayStopsCount, key=subwayStopsCount.get)
    print (f"Route with the least stops: {minStopsRoute} has {subwayStopsCount[minStopsRoute]} stops.")
    #print (stopsResp.json())
    #print(stops)
    
    print ("\n******************** Stops that connect two or more subway routes ********************")
    for stopName in stops:
        #debug
        #print (f"Number of routes that stop in {stopName} = {len(stops[stopName])}")
        if len(stops[stopName]) > 1:
            print (f"{stopName} connects: {', '.join(stops[stopName])}")
    #debug:
    print (f"\nBostonSubway Graph: {bostonSubway}")
    print (f"Sample edge with data: Revere Beach -> Wonderland  = {bostonSubway.edges['Revere Beach','Wonderland']}")
    #This is the solution to question #3: List a rail route you could travel to get from one stop (src) to the other (dest).
    path = nx.shortest_path(bostonSubway, source="Ashmont", target="Arlington")
    routeList = set()
    prevStop = None
    for p in path:
        if prevStop is not None:
            routeList.add(bostonSubway.edges[prevStop, p]['route'])
        prevStop = p
    print (f"Path found: {path} | Routes used: {routeList}")

def upsertValuesToDict(uDict, uKey, uValues):
    #Upsert values to dictionary where value is a list
    if uKey not in uDict:
        uDict[uKey] = list()
    uDict[uKey].extend(uValues)
    return uDict

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
    print ("python3 compass.py -r <showAllRoutes:string> -s <showStopsInfo:string> -f <findRoutes:string> -v")
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
