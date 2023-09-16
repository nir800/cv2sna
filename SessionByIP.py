
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


MY_IP = input(blue("Please enter IP address: "))
print(red(f"+++++++++++++++++++++++++++++++++++++++++"))


19
def is_valid_ipv4_address(address):
     try:
         ipaddress.IPv4Address(address)
         return True
     except ipaddress.AddressValueError:
         return False
     
if is_valid_ipv4_address(MY_IP):
    url = "https://" + ISE_IP + "/admin/API/mnt/Session/EndPointIPAddress/" + MY_IP
    payload = {}
    headers = {
    'Accept': 'application/xml'
    }
    response = requests.get(url=url, auth=auth, headers=headers, verify=False)
    xml_data1 = response.text
    # Parse the XML data using ElementTree
    root = ET.fromstring(xml_data1)
    # Extract the information from XML
    nas_port_id = root.find('nas_port_id').text
    calling_station_id = root.find('calling_station_id').text
    network_device_name = root.find('network_device_name').text
    user_name = root.find('user_name').text
    identity_group = root.find('identity_group').text
    print(green(f"Switch Name: {network_device_name}"))
    print(green(f"Switch Port ID: {nas_port_id}"))
    print(yellow(f"Endpoint MAC: {calling_station_id}"))
    print(yellow(f"Username/Hostname: {user_name}"))
    print(yellow(f"Device Type: {identity_group}"))
        
else:
    print(red(f"{MY_IP} is a valid IP address."))
    


