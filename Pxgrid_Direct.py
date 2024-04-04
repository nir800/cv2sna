
__version__ = "1.2"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"

""" 
Nir Rephael - Bynet Data Communication
"""


import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET
import ipaddress
import pandas as pd
import json
from crayons import blue, red, green, yellow
from dotenv import dotenv_values
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



# Import env variables from dotenv file .env 

config = dotenv_values(".env1")

ISE_IP = config.get("ISE_IP")
ISE_USER = config.get("ISE_USER")
ISE_PASSWORD = config.get("ISE_PASSWORD")
auth = HTTPBasicAuth(ISE_USER, ISE_PASSWORD)

base_url = "https://" + ISE_IP + ":443/api/v1/pxgrid-direct/"

connector_name = input(blue("Connector name is: "))
command = input(blue("Please enter status or update: "))
print(red(f"+++++++++++++++++++++++++++++++++++++++++"))




auth = HTTPBasicAuth(ISE_USER, ISE_PASSWORD)
headers = {"Content-Type": "application/json",
           "Accept": "application/json"}


if command == "status":
    url = base_url + "syncNowStatus/" + connector_name
    response = requests.get(url=url, auth=auth, headers=headers, verify=False)
    info = (response.content)
    info_data = info.decode("utf-8")
    formatted_data = json.loads(info_data)
    connector_name = formatted_data['response']['connector']['connectorName']
    sync_status = formatted_data['response']['connector']['syncStatus']
    print(connector_name, sync_status)
elif command =="update":
    url = base_url + "syncnow"
    data = {
    "connector": {
        "SyncType": "FULL",
        "connectorName": connector_name,
        "description": "description"
        }
    }
    response = requests.post(url, auth=auth, headers=headers, json=data, verify=False) 
    print(response.content)
     

    if response.status_code == 200:
        print("Request successful.")
        print("Response:")
        print(response.json())
    else:
        print("Request failed with status code:", response.status_code)
    
else:
    print (red(f"wrong vlaue!!!"))





    