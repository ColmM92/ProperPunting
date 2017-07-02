# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 22:24:36 2016

@author: lorrieq
"""

import urllib
import urllib.request
import urllib.error
import datetime as dt
import json
import sys


def callAPI(sessionId, r):
    r = r.encode('utf-8')
    try:
        url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        headers = {'X-Application': 'jUb7WvYZenetooca',
                   'X-Authentication': sessionId,
                   'content-type': 'application/json'}
        req = urllib.request.Request(url, r, headers)
        response = urllib.request.urlopen(req)
        jsonresp = response.read()
        return jsonresp
    except urllib.request.URLError as e:
        print('Oops issue with request')
        sys.exit(1)
    except urllib.request.HTTPError:
        print('Oops issue with request')
        sys.exit(1)


def listToAPIString(pieces):
    piece_str = ''
    for piece in pieces:
        piece_str += '"{}", '.format(piece)
    return piece_str[:-2]


def get_market_catalogue(eventType, countries, mtype, projections):
    now = dt.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    return '{"jsonrpc": "2.0", ' \
        '"method": "SportsAPING/v1.0/listMarketCatalogue",' \
        '"params": {"filter":{"eventTypeIds":["' + eventType + '"],' \
        '"marketCountries":[' + listToAPIString(countries) + '],"marketTypeCodes":["' + mtype + '"],' \
        '"marketStartTime":{"from":"' + now + '"}}, "sort":"FIRST_TO_START",' \
        '"maxResults": "100",' \
        '"marketProjection":[' + listToAPIString(projections) + ']},' \
        '"id": 1}'


def get_market_book(sessionId, ids):
    id_list = '","'.join(ids)
    req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook",' \
        '"params": {"marketIds": ["' + id_list + '"],' \
        '"priceProjection":{"priceData":["EX_BEST_OFFERS"]}, "maxResults": "100"}, "id": 1}'
    data = callAPI(sessionId, req)
    return get_result(data)


def get_result(data):
    data = json.loads(data.decode('utf-8'))
    try:
        data = data['result']
        return data
    except:
        print('Exception extracting result')
        print(data)
        sys.exit(1)
