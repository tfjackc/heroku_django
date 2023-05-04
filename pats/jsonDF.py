from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import requests
import pandas as pd


def valuation(name):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property_values/FeatureServer/0/query"

    searched_name = name.upper()
    where_clause = f"owner_name LIKE '%{searched_name}%'"
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


    #print(jsonValueResponse.keys())

   #print(jsonValueResponse)

    #print(type(jsonValueResponse))

    df_list = []
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                attributes_dict = feature['attributes']
                df = pd.DataFrame.from_dict(attributes_dict, orient='index').T
                df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)

    #return df
    print(df)
        
    #df = pd.DataFrame.from_dict(jsonValueResponse, orient='tight')
    #print(df)


valuation('smith')