
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



ISE_IP = "192.168.103.4"
ISE_USER = "admin"
ISE_PASSWORD = "1q2w3e4rT"
auth = HTTPBasicAuth(ISE_USER, ISE_PASSWORD)

url = "https://" + ISE_IP + "/admin/API/mnt/Session/ActiveList"
payload = {}
headers = {
    'Accept': 'application/xml'
    }
response = requests.get(url=url, auth=auth, headers=headers, verify=False)
print (response.content)
