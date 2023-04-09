import requests
import json

# 1. Ask for traffic data in a 6 NM radius around Hessa's tip
# using https://datalastic.com/api-reference/ and save to a
# json file

# Hessa's tip coordinates from Google maps
# lat, long
# 62.463511052700106, 6.170671871147096

# Enter your secret API key below
# (preferably as an environment variable)
API_key = ''

params = {
    'api-key': API_key,
    'lat': 62.463511052700106,
    'lon': 6.170671871147096,
    'radius': 6
}

method = 'vessel_inradius'
api_base = 'https://api.datalastic.com/api/v0/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()

sample = json.dumps(api_response, indent=4, sort_keys=True)
print(sample)

with open('sample.json', 'w') as outfile:
    outfile.write(sample)

# 2. Load from a json file
# (this is good for handling and troubleshooting static
# data because it does not use our quota of API calls)

sample_in = open('sample.json')
sample_in_dict = json.load(sample_in)
sample_in_pretty = json.dumps(sample_in_dict, indent=4)

print(sample_in_pretty)

# 3. Get dimension data for the vessels found
# and save to a json file

vessel_specs = {}

for values in sample_in_dict['data']['vessels']:
    uuid = values['uuid']

    params = {
        'api-key': API_key,
        'uuid': uuid
    }

    method = 'vessel_info'
    api_base = 'https://api.datalastic.com/api/v0/'
    api_result = requests.get(api_base+method, params)
    api_response = api_result.json()

    vessel_specs[uuid] = {}
    vessel_specs[uuid]['data'] = api_response['data']

sample_specs = json.dumps(vessel_specs, indent=4, sort_keys=True)
print(sample_specs)

with open('sample_specs.json', 'w') as outfile:
    outfile.write(sample_specs)

# 4. Inspect how much API calls we have in our quota

params = {
    'api-key': API_key
}

method = 'stat'
api_base = 'https://api.datalastic.com/api/v0/'
api_result = requests.get(api_base+method, params)
api_response = api_result.json()

print(api_response)

# 5. The fifth and last step for the live maneuvering dashboard
# would be to send the vessel list and specs to the client over WebSockets
# However, this type dynamic behaviour is not supported on static GitHub pages
# as far as I know, so unfortunately I will need to load vessel data directly
# on the webpage without direct integration with the API :(
