#!/usr/bin/python

import requests
from tqdm import tqdm
import threading
import time
import pandas as pd
import cPickle as pickle


def _get_ip_intel(ip_addr):
    """
    Query Virustotal with the suspicious IP and add it to the list iof malicious IPs if positive

    :param Flow flow: A data flow record
    :param ip_addr: Suspicious IP address
    :return:
    """
    if ip_addr == '':
        ip_scores[ip_addr] = pd.NaT

    else:
        ip_params = {'ip': ip_addr, 'contact': 'vkarthy1@jhu.edu', 'format': 'json'}

        response = requests.get('http://jhum0ud74roypfyvtpr.getipintel.net/check.php',
                                params=ip_params)

        ip_score = response.json()['result']
        ip_scores[ip_addr] = ip_score

    pickle.dump(ip_scores, open('ip_scores.pickle', 'wb'))

    return


ip_addrs = pickle.load(open('ip_address.pickle', 'rb'))
ip_scores = pickle.load(open('ip_scores.pickle', 'rb'))

count = 0

print ip_scores['221.122.101.203']

