# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 11:01:07 2016

@author: lorrieq
"""

import sys
import getopt
import datetime as dt
from oddschecker.horse_racing import GB_IE as oddscheckerGBIE
from main_scripts.horse_racing import common
from general import common_functionality as cf
from db_interact import select, update, insert, delete

sportId = select.sportId("Horse Racing")
entities = {}
winId = select.productId("Win")
priceId = select.valueTypeId("Price")
kellyId = select.valueTypeId("Kelly")
growthId = select.valueTypeId("Growth")
oddscheckerId = select.sourceIdForName("Oddschecker")
properPuntingId = select.sourceIdForName("Proper Punting")

def getVenueId(venueInfo, name, time):
    for entry in venueInfo:
        entry_time = entry['VN_Datetime']
        entry_time = str(entry_time.time().strftime('%H:%M'))
        if entry['VN_Name'] == name and entry_time == time:
            return entry['VN_ID']


def readPrices(venueName):
    prices = oddscheckerGBIE.getPrices(venueName)
    if prices is None:
        return
    for entry in prices:
        for horse, odd in entry[2]:
            entityId = entities[horse][0]
            if '(N/R)' in horse:
                continue
            num_odd = cf.fraction_str_to_decimal(odd)
            if num_odd is not None and num_odd != entities[horse][1]:
                entities[horse][1] = num_odd
                # reset kelly / growth
                insert.fact(entityId, properPuntingId, kellyId, winId, 0.0)
                insert.fact(entityId, properPuntingId, growthId, winId, 0.0)
                insert.fact(entityId, oddscheckerId, priceId, winId, num_odd)
    return


def endActions(run):
    today = dt.date.today()
    update.removeKellyGrowth(sportId, today)


def main(run):
    global entities
    today = dt.date.today()
    venueNames = select.venueNames(sportId, today)
    entities = cf.getEntityDict(today, 'Horse Racing', ('GB', 'IE'))
    while True:
        for venue in venueNames:
            readPrices(venue['VN_Name'])
        print('oddschecker loop at {} utc'.format(dt.datetime.utcnow()))
        if dt.datetime.utcnow() > stop:
            break
    endActions(run)
    print('done')


if __name__ == '__main__':
    run, stop = cf.hour_setup(getopt.getopt(sys.argv[1:], 'h:', ['hour=']))
    main(run)
