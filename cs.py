
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



# Define the URL

# /devices/queries/devices-scroll/v1
# curl -X GET "https://api.us-2.crowdstrike.com/devices/queries/devices-scroll/v1" -H  "accept: application/json" -H  "authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InB1YmxpYzo3ODdlZjkxZC01YzMxLTQ3YzktYjg0Ni1kNDIzNTk1M2FmYWEiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOltdLCJjbGllbnRfaWQiOiJlYzYxYjFhOTE2OTQ0YzdjYmM3Y2Y5N2JhYTA5NDMwOSIsImV4cCI6MTY5NTc0Njc3NSwiZXh0Ijp7InN1Yl90eXBlIjoiY2xpZW50In0sImlhdCI6MTY5NTc0NDk3NSwiaXNzIjoiaHR0cHM6Ly9hcGkuY3Jvd2RzdHJpa2UuY29tLnRvZG8vIiwianRpIjoiYzBhNTEyZDYtY2FmNC00MDdkLTkwMjctYzFmZjQwMDRhYTQ0IiwibmJmIjoxNjk1NzQ0OTc1LCJzY3AiOltdLCJzdWIiOiJlYzYxYjFhOTE2OTQ0YzdjYmM3Y2Y5N2JhYTA5NDMwOSIsInN1Yl90eXBlIjoiY2xpZW50In0.GSJJwFB2Xqt41XUDlOM7Ihs8Aknn6n1z9eRkhcbgocdjcxkN6euk95ZqiQQTZm9j-nZQkAqluZ3qBAxIgrfHW520W35ytGJRKidpyKTXOoOiIhf41XV1ySYZ4j68haaLuBTcloKbG5ERB4OhosA006-Cj5ZVFrBbkA-eLr_anX1sjDioWY3h-tw4oK0z60kAEMhLidMLRPfkfLyg358CCzXfijbqhElHP89a0fN_p9PMH1oQmHxjKsadaLQADAtaUB0rI99BAoC8_KN5L1OZOpY75sZyDeuicm4LsVCalj93qS8kiCO7W9Gp6rvLk9MAzdHTlrLXpnzYoN_xydlXxEeBnjyk8J7ypMowU3HPyn7MCoQVmthiIbOYQbRMRyw8YGQtN0BcX3FjWygbETJVEbekB4QbfwJrkLK95r9xbZuwEZw694dI2Vx-1R9SquGw-nQuOpNtjpTghRunCWzk_9pKUjAjzsnaHhg5vNdi1bWBbfW01MMQ2fgp7QMwseyG9NQLoIw5JiFw7jzRgzcjPwfklwAp8H-nNrMHrRaqx2bLY66IhsyZSRu5WWCxayKkzuWURRhN9jsRzWqWydBrZ1DMFwP1M4PFNBfJbo1vjSdUC3gLYvzW7LZBnnuzdYeC0WR3vzUbOqKRHXtvs7-lkCZnibgT9i7A5p41tnjsVJA"
# url = "https://api.us-2.crowdstrike.com/falcon-complete-dashboards/queries/detects/v1" 
# url = "https://api.crowdstrike.com/detects/queries/detects/v1?limit=1000"
url = "https://api.eu-1.crowdstrike.com/detects/queries/detects/v1?status=in_progress"
# url = "https://api.eu-1.crowdstrike.com/falcon-complete-dashboards/queries/detects/v1"


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
    ldt_values = response_data['resources']
    for ldt in ldt_values:
        print(ldt)
else:
    # Request failed
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)
