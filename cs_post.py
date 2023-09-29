
__version__ = "1.2"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"

""" 
Nir Rephael - Bynet Data Communication
"""


import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import json
from crayons import blue, red, green, yellow
from dotenv import dotenv_values
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from prettytable import PrettyTable
import shutil

# Create a new table
table = PrettyTable()


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
    data = response.json()
else:
    print(f"Request failed with status code {response.status_code}")
    print("Response content:")
    print(response.text)
hostname = data['resources'][0]['device']['hostname']
filepath = data['resources'][0]['behaviors'][0]['filepath']
local_ip = data['resources'][0]['device']['local_ip']
timestamp = data['resources'][0]['behaviors'][0]['timestamp']
technique = data['resources'][0]['behaviors'][0]['technique']
cmdline = data['resources'][0]['behaviors'][0]['cmdline']
filename = data['resources'][0]['behaviors'][0]['filename']
severity = data['resources'][0]['behaviors'][0]['severity']
parent_cmdline = data['resources'][0]['behaviors'][0]['parent_details']['parent_cmdline']
description = data['resources'][0]['behaviors'][0]['description']
status = data["resources"][0]["status"]

print(hostname)
print(filepath)


# Define the table columns
# table.field_names = ["Hostname", "Filepath", "Local IP", "Timestamp", "Technique", "CMD Line", "Filename", "Severity", "Parent CMD", "Description"]

# Add data to the table
# table.add_row([hostname, filepath, local_ip, timestamp, technique, cmdline, filename, severity, parent_cmdline, description])

# Print the table
# print(table)


# Get the terminal width
terminal_width, _ = shutil.get_terminal_size()

# Create a new table
table = PrettyTable()

# Define the table columns
table.field_names = ["Hostname", "Local IP", "Status", "Technique", "CMD Line", "Filename", "Severity", "Parent CMD"]

# Add data to the table
table.add_row([hostname, local_ip, status, technique, cmdline, filename, severity, parent_cmdline])

# Set the max width of the table to fit the terminal window
table.max_width = terminal_width

# Print the table
print(green(table))



