from os import access
import config
import requests
import base64
import json
import pandas as pd

def get_access_token():
    url = config.auth_url
    body = f'grant_type=refresh_token&refresh_token={config.refresh_token}'
    base64_message = f'{config.client_id}:{config.client_secret}'
    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64encode(base64_bytes)
    message = message_bytes.decode('utf-8')
    headers = {'Authorization' : f'Basic {message}', 
               'Content-Type' : 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=body, headers=headers)
    res_json = response.json()
    if 'access_token' not in res_json:
        print('Refresh Token Expired')
        exit()
    return res_json['access_token']

def query_helper(query):
    resource = '/query'
    url = f'{config.base_url}/v3/company/{config.company_id}{resource}?minorversion=63'
    headers = {'Authorization' : f'Bearer {access_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/text',
    }
    response = requests.post(url, headers=headers, data=query)
    return response

def main(access_token):
    qb_object = config.qb_object
    limit = 1000
    query_count = f'select Count(*) from {qb_object} maxresults {limit}'
    count_response = query_helper(query_count)
    count_total = count_response.json()['QueryResponse']['totalCount']
    print(f'Total Count: {count_total}')

    query = f'select * from {qb_object} maxresults {limit}'
    inital_response = query_helper(query)
    df = pd.read_json (json.dumps(inital_response.json()['QueryResponse'][qb_object]))

    extra_runs = count_total // limit
    for i in range(extra_runs):
        extra_query = f'select * from {qb_object} maxresults {limit} STARTPOSITION {(i+1) * limit}'
        extra_response = query_helper(extra_query)
        new_df = pd.read_json (json.dumps(extra_response.json()['QueryResponse'][qb_object]))
        df = pd.concat([df, new_df])
    df.to_csv (f'{qb_object.lower()}.csv', index = None)

if __name__ == '__main__':
    access_token = get_access_token()
    main(access_token)