
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
url = "https://api.us-2.crowdstrike.com/oauth2/token"

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
response = requests.post(url, headers=headers, data=data)

response_data = response.json()
access_token = response_data.get("access_token")
print("Access Token:", access_token)



# Define the URL
url = "https://api.us-2.crowdstrike.com/falcon-complete-dashboards/queries/detects/v1"

# Define the headers, including the authorization header with the bearer token
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {access_token}"
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    # Request was successful
    response_data = response.json()
    # Process the response data as needed
    print("Response Data:", response_data)
else:
    # Request failed
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)
