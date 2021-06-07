# Feature collector "traffic-fc"
***Version:*** 1.0

***Date:*** 21.05.2021

***Authors:***  [Zisis Maleas](https://github.com/zisismaleas); [Panagiotis Tzenos](https://github.com/ptzenos)

***Address:*** The Hellenic Institute of Transport (HIT), Centre for Research and Technology Hellas (CERTH)

# Description 

The "traffic-fc" feature collector is  a module of the **Ride2Rail Offer Categorizer** responsible for the computation of the determinant factors: ***"traffic"***. 

To calculate the ***"requests_dict_norm"*** determinant factor, this feature collector relies on the ***HERE Traffic API(https://developer.here.com)***. A HERE Developer account is required and an API Key needs to be inserted in the file ***["traffic.conf"](https://github.com/Ride2Rail/traffic-fc/blob/main/code/traffic.conf)***.

Computation can be executed from ***["traffic.py"](https://github.com/Ride2Rail/traffic-fc/blob/main/traffic.py)*** by running the procedure ***extract()*** which is binded under the name ***compute*** with URL using ***[FLASK](https://flask.palletsprojects.com)*** (see example request below).

 Computation is composed of three phases (***Phase I:***, ***Phase II:***, and 
***Phase III:***) in the same way the ***(https://github.com/Ride2Rail/tsp-fc)*** use it.

As a categorization of the level of congeestion this trip might face: 
***ratio*** : Duration with current Flow / Duration with Free Flow. 
The higher the ratio the worst the traffic condition. The traffic status calculated only in cases where
the trasport mode must use road network. The categorization range from 1-5 while non-road legs get the
value 6. The values returned in a normalized format.


# Configuration

The following values of parameters can be defined in the configuration file ***"traffic.conf"***.

Section ***"running"***:
- ***"verbose"*** - if value __"1"__ is used, then feature collector is run in the verbose mode,
- ***"scores"*** - if  value __"minmax_score"__ is used, the minmax approach is used for normalization of weights, otherwise, the __"z-score"__ approach is used.
- ***"Here_API_Key"*** - A valid and active API Key from **HERE Traffic API(https://developer.here.com)***

Section ***"cache"***: 
- ***"host"*** - host address where the cache service that should be accessed by ***"traffic-fc"*** feature collector is available
- ***"port"*** - port number where the cache service that should be accessed used by ***"traffic-fc"*** feature collector is available

**Example of the configuration file** ***"traffic.conf"***:
```bash
[service]
name = traffic
type = feature collector
developed_by = Zisis Maleas <https://github.com/zisismaleas> and Panagiotis Tzenos <https://github.com/ptzenos>

[running]
verbose = 1
scores  = minmax_scores
Here_API_Key  = HEREAPIKEY

[cache]
host = cache
port = 6379
```

# Usage
### Local development (debug on)

The feature collector "traffic-fc" can be launched from the terminal locally by running the script "traffic.py":

```bash
$ python3 traffic.py
 * Serving Flask app "traffic" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 
```

Moreover, the repository contains also configuration files required to launch the feature collector in Docker from the terminal by the command docker-compose up:

```bash
docker-compose up
Starting traffic_fc ... done
Attaching to active_fc
traffic_fc    |  * Serving Flask app "traffic.py" (lazy loading)
traffic_fc    |  * Environment: development
traffic_fc    |  * Debug mode: on
traffic_fc    |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
traffic_fc    |  * Restarting with stat
traffic_fc    |  * Debugger is active!
traffic_fc    |  * Debugger PIN: 
```

### Example Request
To make a request (i.e. to calculate values of determinant factors assigned to the "traffic-fc" feature collector for a given mobility request defined by a request_id) the command curl can be used:
```bash
$ curl --header 'Content-Type: application/json' \
       --request POST  \
       --data '{"request_id": "123x" }' \
         http://localhost:5006/compute
```
