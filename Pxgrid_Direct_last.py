
__version__ = "1.4"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"
__Utils__= "Pxgrid direct check status and manual sync"

""" 
Nir Rephael - Bynet Data Communication
"""
import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import json
from crayons import blue, red  
from dotenv import dotenv_values
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Import env variables from dotenv file .env 
config = dotenv_values(".env1")

ISE_IP = config.get("ISE_IP")
ISE_USER = config.get("ISE_USER")
ISE_PASSWORD = config.get("ISE_PASSWORD")
auth = HTTPBasicAuth(ISE_USER, ISE_PASSWORD)

base_url = f"https://{ISE_IP}:443/api/v1/pxgrid-direct/"

headers = {"Content-Type": "application/json", "Accept": "application/json"}

def get_connector_status(connector_name):
    url = base_url + "syncNowStatus/" + connector_name
    try:
        response = requests.get(url=url, auth=auth, headers=headers, verify=False)
        response.raise_for_status()
        formatted_data = response.json()
        connector_name = formatted_data['response']['connector']['connectorName']
        sync_status = formatted_data['response']['connector']['syncStatus']
        print(red(f"Pxgrid Direct Connector {connector_name}: {sync_status}"))
        
    
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def update_connector(connector_name):
    url = base_url + "syncnow"
    data = {
        "connector": {
            "SyncType": "FULL",
            "connectorName": connector_name,
            "description": "description"
        }
    }
    
    try:
        response = requests.post(url, auth=auth, headers=headers, json=data, verify=False)
        response.raise_for_status()
        print("Request successful.")
        print("Response:")
        print(red(response.json()))
    except requests.exceptions.RequestException as e:
        print("Request failed with status code:", response.status_code, "Error:", e)

# Main execution logic
if __name__ == "__main__":
    while True:
        (red(f"wrong vlaue!!!"))
        print(blue(f"+++++++++++++++++++++++++++++++++++++++++"))
        print("1. Status")
        print("2. Update")
        print("3. Exit")
        choice = input(blue(f"Please choose an option (1/2/3): "))

        if choice == '1':
            connector_name = input("Connector name is: ")
            get_connector_status(connector_name)
        elif choice == '2':
            connector_name = input("Connector name is: ")
            update_connector(connector_name)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please try again.")