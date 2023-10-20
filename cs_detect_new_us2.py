
__version__ = "1.2"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"

""" 
Nir Rephael - Bynet Data Communication
https://api.us-2.crowdstrike.com  This is the base URL 
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

config = dotenv_values(".env3")

client_id = config.get("client_id")
secret_key = config.get("secret_key")


# Define the URL for access token
url = "https://api.us-2.crowdstrike.com/oauth2/token"
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
# print("Access Token:", access_token)






def fetch_crowdstrike_data(ids):
    url = "https://api.us-2.crowdstrike.com/detects/entities/summaries/GET/v1"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    data = {
        "ids": [ids]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
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


        if status == "new":

            
            table = PrettyTable()
            table.border = True
            # Add data to the table as separate rows
            table.field_names = ["Attribute", "Value"]
            table.add_row(["Timestamp", timestamp])
            table.add_row(["Hostname", hostname])
            table.add_row(["Local IP", local_ip])
            table.add_row(["Status", status])
            table.add_row(["Technique", technique])
            table.add_row(["CMD Line", cmdline])
            table.add_row(["Filename", filename])
            table.add_row(["Severity", severity])
            table.add_row(["Parent CMD", parent_cmdline])

            # Set the max width of the table to fit the terminal window
            terminal_width, _ = shutil.get_terminal_size()
            table.max_width = terminal_width

            # Customize the table view (optional)
            table.align["Attribute"] = "l"  # Left-align the Attribute column

            # Print the table
            print(green(table))
            
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response content:")
        print(response.text)
        return None

    

url = "https://api.us-2.crowdstrike.com/detects/queries/detects/v1?limit=100"


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
   # print("Response Data:", response_data)
    ldt_values = response_data['resources']
    for ldt in ldt_values:
        fetch_crowdstrike_data(ldt)
else:
    # Request failed
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.text)


# End 
