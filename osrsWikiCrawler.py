import pandas as pd
import json
import urllib.request

def create_request(url_in):
    '''Create request with given url.'''
    req = urllib.request.Request(
        url = url_in, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
        }
    )
    return req

def create_time_series_url(inc, id):
    '''Create timeseries API url for item id with inc steps.'''
    return "https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep={}&id={}".format(inc, id)

def get_mapping_data(id_data):
    '''Get data from mapping API and save to id_data'''
    mapping_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    req = create_request(mapping_url)

    # get data from API
    with urllib.request.urlopen(req) as response:
        # convert response to json list of dicts
        data_json = json.loads(response.read())

        # convert json to dict(key = item_id, val = timestamp dict)
        for row in data_json:
            item_id = row['id']

            # add item_id to dict if not already added
            id_data[item_id] = [row]


def get_time_series_data(inc, item_id):
    '''Get timeseries API data for item_id.'''
    req = create_request(create_time_series_url(inc, item_id))

    # get timeseries for item_id from API
    with urllib.request.urlopen(req) as response:
        data_json = json.loads(response.read())
        
        # return list of timestamp dicts
        return data_json['data']


def create_time_series_txt():
    '''Save API data to time_series_data_2.txt, where json_dict[item_id][0] = mapping_dict and [1] = timeseries_list.'''
    # get data from mapping API
    id_data = {}
    get_mapping_data(id_data)

    inc = '6h'
    id_count = 0

    # get timeseries data for each item_id from API
    for item_id in id_data:
        # print progress
        print("{}\tid #{}".format(id_count, item_id))
        id_count += 1

        id_data[item_id].append(get_time_series_data(inc, item_id))

    # write data to a .txt
    txt_filename = 'time_series_data_6h_4-8-22.txt'
    with open(txt_filename, 'w+') as f:
        f.write(json.dumps(id_data))



create_time_series_txt()