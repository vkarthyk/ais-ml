import pandas as pd
import json
import hashlib
import time
import requests
import time
import cPickle as pickle
from tqdm import tqdm
import threading

API_KEY = '3741ba28d0f665aa3ba95ebd41b1750986803fa81f3f0da93483657db8cb16bd'

df = pd.read_csv('final_final_feature_set.csv', encoding='ISO-8859-1')
df.info()
df = df.fillna('')


def _get_hash_score(hash_value):
    malicious_level = 0.0
    if hash_value != '':
        
        params = {'apikey': API_KEY, 'resource': hash_value}
        headers = {
          "Accept-Encoding": "gzip, deflate",
          "User-Agent" : "gzip,  My Python requests library example client or username"
          }
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
          params=params, headers=headers)
        json_response = response.json()
        time.sleep(0.11)
        if json_response['response_code'] == 1:
            positives = json_response["positives"]
            total = json_response["total"]
            malicious_level += positives / float(total)
        else:
            malicious_level = pd.NaT
    else:
        malicious_level = pd.NaT
                
    return malicious_level


df['hash_score'] = df['observable.object.properties.hashes.simple_hash_value.value'].apply(lambda x: _get_hash_score(x))
df['hash_score'].describe()


url_scores = pickle.load(open('url_score_dict.pickle', 'rb'))


def _get_url_score(url):
    malicious_level = 0.0
    try:
        params = {'apikey': API_KEY, 'resource': url}
        headers = {
          "Accept-Encoding": "gzip, deflate",
          "User-Agent" : "gzip,  My Python requests library example client or username"
          }
        response = requests.get('https://www.virustotal.com/vtapi/v2/url/report',
          params=params, headers=headers)
        json_response = response.json()
        if json_response['response_code'] == 1:
            positives = json_response["positives"]
            total = json_response["total"]
            malicious_level += positives / float(total)
            url_scores[url] = malicious_level
            pickle.dump(url_scores, open('url_score_dict.pickle', 'wb'))
            return
        
    except ValueError as e:
        return


for url in tqdm(df['observable.object.properties.value.value']):
    if url != '':
        if type(url_scores[url]) == float:
            time.sleep(2)
            t = threading.Thread(target=_get_url_score, args=(url,))
            t.start()
