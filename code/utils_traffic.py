import numpy as np 
from hereAPI.routing_API import *
import json
from r2r_offer_utils  import normalization


def categorizeCongestion(ratio): 
    '''
    There are 5 categories : [ <1 , 1-1.3, 1.3 - 1.6, 1.6 - 2, >2]

    ''' 
    if ratio < 1 : 
        return 5 
    elif ratio < 1.3:
        return 4 
    elif ratio < 1.6: 
        return 3 
    elif ratio < 2:
        return 2 
    else: 
        return 1


def transformStringToNum (data): 

    offer_keys = data['output_offer_level']['offer_ids']

    for offer in offer_keys: 

        trip_legs  = data['output_tripleg_level'][offer]['triplegs']

        data['output_offer_level'][offer]['num_interchanges'] = \
            int(data['output_offer_level'][offer]['num_interchanges'])

        for leg in trip_legs:
            data['output_tripleg_level'][offer][leg]['leg_stops'] = \
                json.loads(data['output_tripleg_level'][offer][leg]['leg_stops'])
            try:
                data['output_tripleg_level'][offer][leg]['leg_track'] = \
                    json.loads(data['output_tripleg_level'][offer][leg]['leg_track'])
            except:
                pass
    return data

def computeTraffic(key, origin, destinaton, timestamp):
    #print(key, origin, destinaton, timestamp)
    #r_api = routing_API() r_api.

    sample_req = get_route_info(key, origin, destinaton, timestamp)

    return sample_req['Status'], sample_req['RtToFf'], sample_req['AvgSpeed']

def has_car(Offer): 
    legKeys = Offer['triplegs']
    if not len(legKeys) == 0: 
        for legkey in legKeys:  
            if Offer[legkey]['transportation_mode'] in ['car', 'taxi', 'self-drive-car', 'truck', 'bus']: 
                return True
                break
    return False

def get_traffic_level(Offer, key):
    count = 0 
    cong = 0
    legKeys = Offer['triplegs']
    if not len(legKeys) == 0: 
        for legkey in legKeys:  
            if Offer[legkey]['transportation_mode'] in ['car', 'taxi', 'self-drive-car', 'truck', 'bus']:

                origin = Offer[legkey]['leg_stops']['coordinates'][0] 

                destinaton = Offer[legkey]['leg_stops']['coordinates'][1] 
                
                origin[0], origin[1] = origin[1], origin[0]
                destinaton[0], destinaton[1] = destinaton[1], destinaton[0]

                timestamp = Offer[legkey]['start_time']

                is_valid, criticalRatio, avg_speed = computeTraffic(key, origin, destinaton, timestamp)
                
                if is_valid == 'ok':
                    count += 1
                    cong += categorizeCongestion(criticalRatio)
                    return np.round(cong/count , 2)
                else:
                    return 0                



def trafficCollect(data, key, SCORES = "minmax_scores"):
    '''
    For each offer returns the congestion level (1:High - 5: Low) that trip will face: 

    The offers without car will automatically take the value 6

    ''' 
    data = transformStringToNum(data)
    req = data['output_tripleg_level']
    requests_dict = {}
    offer_keys = list(req.keys())
    print(offer_keys)
    for one_offer in  offer_keys:
        temp_offer = req[one_offer] 
        if has_car(temp_offer): 
            temp_traffic_volume = get_traffic_level(temp_offer, key)
            requests_dict[one_offer] = float(temp_traffic_volume)
        else: 
            requests_dict[one_offer] = int(6)

    if SCORES == "minmax_scores":
        # calculate minmax scores
        requests_dict_norm        = normalization.minmaxscore(requests_dict)
    else:
        # by default z-scores are calculated
        requests_dict_norm        = normalization.zscore(requests_dict)


    return {'traffic' : requests_dict_norm}       
''' 
    output : 
        traffic_ratio : "time/free_flow_time" 
''' 
