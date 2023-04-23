from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests


def valuation(account):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property_values/FeatureServer/0/query"

    where_clause = f"account_id = {account}"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    url_value = f"{propValue_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"

    # set variables
    response = requests.get(url)
    responseValue = requests.get(url_value)
    jsonResponse = response.json()
    jsonValueResponse = responseValue.json()

    # set empty lists
    maptaxlot = []
    structure = []
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                mt = feature['attributes']['map_taxlot']
                mt_find = mt[:mt.find('-', mt.find('-') + 1)]
                maptaxlot.append(mt_find.replace('-', ''))

                struc = int(feature['attributes']['rmv_total'])-int(feature['attributes']['rmv_land'])
                structure.append(struc)

    # set empty dictionaries
    real_market_value = {}
    value_structure = {}
    total_real_market = {}
    max_assessed = {}
    total_assessed = {}
    veterans = {}
    year_list = [2018, 2019, 2020, 2021, 2022]

    for keys, value in jsonValueResponse.items():
        if keys == 'features':
            for feature in value:
                for yr in year_list:
                    if feature['attributes']['year_'] == yr:
                        struc = int(feature['attributes']['rmv_total']) - int(feature['attributes']['rmv_land'])
                        real_market_value[yr] = feature['attributes']['rmv_land']
                        value_structure[yr] = struc
                        total_real_market[yr] = feature['attributes']['rmv_total']
                        max_assessed[yr] = feature['attributes']['max_av']
                        total_assessed[yr] = feature['attributes']['total_av']
                        veterans[yr] = feature['attributes']['exempt']


    context = {'data':jsonResponse, 'value_data':jsonValueResponse, 'maptaxlot': maptaxlot, 'structure':structure, 
    'value_structure':value_structure, 'max_assessed':max_assessed, 'real_market_value':real_market_value, 'total_real_market':total_real_market, 
    'total_assessed':total_assessed, 'veterans':veterans}
    
    return context


def mapRequest(account):

    context = valuation(account)

    print(context)




mapRequest(1001)