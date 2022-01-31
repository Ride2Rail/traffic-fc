#!/usr/bin/env python

from herepy import (
    RoutingApi,
    RouteMode,
    MatrixRoutingType,
    MatrixSummaryAttribute,
    RoutingTransportMode,
    RoutingMode,
    RoutingApiReturnField,
    RoutingMetric,
    RoutingApiSpanField,
    AvoidArea,
    AvoidFeature,
    Avoid,
    Truck,
    ShippedHazardousGood,
    TunnelCategory,
    TruckType,
) 
import logging
import time



def get_route_info(rapi_key, coords_origin, coords_destination, departure_time):
    try:
        # prevent service abuse (minimum 1 sec between requests)
        # time.sleep(1)
        # initialize engine
        arouting_api = RoutingApi(rapi_key)            
        # fetches a driving route between two points
        response = arouting_api.car_route(
        waypoint_a=coords_origin,
        waypoint_b=coords_destination,
        modes=[RouteMode.car, RouteMode.fastest],
        departure=departure_time,
        )
        # get attributes for the "best" possible route
        E=0.001
        route_info = {'Status': 'ok', 'RtToFf': response.as_dict().get('response').get('route')[0].get('summary').get('trafficTime')/(response.as_dict().get('response').get('route')[0].get('summary').get('baseTime')+E), 
                  'AvgSpeed': (response.as_dict().get('response').get('route')[0].get('summary').get('distance')/(response.as_dict().get('response').get('route')[0].get('summary').get('trafficTime')+E))*3.6}
        #print(response, flush=True)
        #print(route_info, flush=True)
        return route_info
    except:
        logging("Error consuming here-API: Make sure that you provided valid input arguments.") 
        return {'Status': 'error', 'RtToFf': None, 'AvgSpeed':None}
