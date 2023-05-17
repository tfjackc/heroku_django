from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import pandas as pd

# set empty lists
maptaxlot = []
df_list = []
data=[]
# set empty dictionaries
real_market_value = {}
value_structure = {}
total_real_market = {}
max_assessed = {}
total_assessed = {}
veterans = {}


def mapPage(request):
        
    return render(request, 'pats/mapPage.html')

def index(request):

    return render(request, 'pats/index.html')

def base(request):

    return render(request, 'pats/base.html')





account_clause = f"account_id = {account}"
name_clause = f"owner_name LIKE '%{searched_name}%'"

def urlQuery(where_clause):

    prop_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property/FeatureServer/0/query"
    propValue_url = "https://geo.co.crook.or.us/server/rest/services/Hosted/PATS_property_values/FeatureServer/0/query"

    searched_name = name.upper()
    where_clause = f"owner_name LIKE '%{searched_name}%'"
    out_fields = "*"
    return_geometry = "false"
    f = "pjson"

    url = f"{prop_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"
    url_value = f"{propValue_url}?where={where_clause}&outFields={out_fields}&returnGeometry={return_geometry}&f={f}"



def accountQuery(account):

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

    
    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                mt = feature['attributes']['map_taxlot']
                mt_find = mt[:mt.find('-', mt.find('-') + 1)]
                maptaxlot.append(mt_find.replace('-', ''))

    global data_dict

    data_dict = {'data':jsonResponse, 'value_data':jsonValueResponse, 'maptaxlot': maptaxlot}

    return data_dict

def account_query(account):

    accountQuery(account)

    jsonResponse = data_dict['data']

    context = {'data':jsonResponse, 'maptaxlot': maptaxlot}

    return context



def tableSearchResults(name):

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

    for keys, value in jsonResponse.items():
        if keys == 'features':
            for feature in value:
                attributes_dict = feature['attributes']
                df = pd.DataFrame.from_dict(attributes_dict, orient='index').T
                df_list.append(df)

    df = pd.concat(df_list, ignore_index=True)
    print(df)

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    html_table = df.to_html(classes='table table-striped', index=False)
    context = {'html_table': html_table, 'd': data}
    
    return context


tableSearchResults('bike')