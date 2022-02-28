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
    return res_json['access_token']

def main(access_token):
    resource = '/query'
    query = 'select * from Item maxresults 1000'
    url = f'{config.base_url}/v3/company/{config.company_id}{resource}?minorversion=63'
    headers = {'Authorization' : f'Bearer {access_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/text',
    }
    response = requests.post(url, headers=headers, data=query)
    print(response.headers)
    
    df = pd.read_json (json.dumps(response.json()['QueryResponse']['Item']))
    df.to_csv ('products.csv', index = None)

if __name__ == '__main__':
    access_token = get_access_token()
    main(access_token)