# Nir Rephael - Get All Sessions
# Account Approved. Password is T4u78yj1A2jcLPnh

import json
import requests
import ssl
import websocket
import re
import mab_cleanup
import datetime
from crayons import blue, red, green
from base64 import b64encode
from time import sleep
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
password = "T4u78yj1A2jcLPnh"


##### *****Service Lookup****** 
r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/ServiceLookup",
                verify=False,
                auth=("pxgridnir",password),
                json={"name":"com.cisco.ise.session"})       
r.raise_for_status()
json_response=r.json()
print(json.dumps(json_response,indent=2))
service_info=r.json()["services"][0]
session_topic=service_info["properties"]["sessionTopic"]
pubsub_service=service_info["properties"]["wsPubsubService"]
RestBaseURL=service_info["properties"]["restBaseURL"]
NodeName=service_info["nodeName"]


# Access to node secret (different from the password we are using for authentication)
##### *****Getting AccessSecert****** 
r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/AccessSecret",
                verify=False,
                auth=("pxgridnir",password),
                json={"peerNodeName":NodeName})       
r.raise_for_status()
json_response=r.json()
#print(json.dumps(json_response,indent=2))
secret=r.json()["secret"]
print(f"Secret is: {secret}")
print(red(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"))
##### *****Getting All Sessions****** 
r=requests.post(f"{RestBaseURL}/getSessions",
                verify=False,
                auth=("pxgridnir",secret),
                json={})     
r.raise_for_status()
json_response=r.json()
# print(json.dumps(json_response,indent=2))
count=0
sessions = json_response['sessions']
df = pd.DataFrame(sessions)
selected_columns = ['timestamp', 'nasIdentifier', 'userName', 'ipAddresses', 'nasPortId']
selected_df = df[selected_columns]
pd.set_option('colheader_justify', 'center')
print(selected_df)

for session in sessions:
    timestamp = session['timestamp']
    state = session['state']
    userName = session['userName']
    nasPortId = session['nasPortId']
    ipAddresses = session['ipAddresses'][0]
    count=count+1
    # Print session details
    print(green("Timestamp:", timestamp))
    print("State:", state)
    print("UserName:", userName)
    print("nasPortId:", nasPortId)
    print("IP Address:", ipAddresses)
    print()
print(red(f"Number of actvice endpoints:{count}"))

