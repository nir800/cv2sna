
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


url = "https://" + ISE_IP + "/admin/API/mnt/Session/EndPointIPAddress/" + MY_IP
