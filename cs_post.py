
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

config = dotenv_values(".env2")

client_id = config.get("client_id")
secret_key = config.get("secret_key")


# Define the URL
url = "https://api.eu-1.crowdstrike.com/oauth2/token"
# url = "https://api.us-2.crowdstrike.com/oauth2/token"

# Define the headers
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Define the payload (data)

data = {
    "client_id": client_id,
    "client_secret": secret_key
}

# Send the POST request
response = requests.post(url, headers=headers, data=data, verify=False)

response_data = response.json()
access_token = response_data.get("access_token")
print("Access Token:", access_token)




url = "https://api.eu-1.crowdstrike.com/detects/entities/summaries/GET/v1"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "authorization": f"Bearer {access_token}"
}


data = {
    "ids": ["ldt:b57b7476f68440beb8d63eb0f2a4cfd5:8590579966"]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("Request was successful")
    print("Response content:")
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response content:")
    print(response.text)
