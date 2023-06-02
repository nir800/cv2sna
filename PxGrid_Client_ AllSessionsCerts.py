# Nir Rephael - Get all active sessions using pxgrid and client certificate


import json
import requests
import ssl
import datetime
from crayons import blue, red, green
from base64 import b64encode
from time import sleep
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# verify=".rootca.cer"
# Create pxgrid client account by using client certificate 
# client name is pxgrid1
while True:
    r=requests.post(f"https://ise32.cyber.lab:8910/pxgrid/control/AccountActivate",
        cert=("pxgrid1.cer","pxgrid2.key"),
        verify=False,
        auth=("pxgrid1","none"),
        json={}
    )
    r.raise_for_status()
    json_response=r.json()
    print(json.dumps(json_response,indent=2))
    if json_response["accountState"]=="ENABLED":
        print("Account Approved")
        break
    sleep(60)

##### *****Service Lookup****** 
r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/ServiceLookup",
                cert=("pxgrid1.cer","pxgrid2.key"),
                verify=False,
                auth=("pxgrid1","none"),
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
                cert=("pxgrid1.cer","pxgrid2.key"),
                verify=False,
                auth=("pxgrid1","none"),
                json={"peerNodeName":NodeName})       
r.raise_for_status()
json_response=r.json()
#print(json.dumps(json_response,indent=2))
secret=r.json()["secret"]
print(f"Secret is: {secret}")
print(red(f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"))



##### *****Getting All Sessions****** 
# Using API to get all active session, using the secret.
r=requests.post(f"{RestBaseURL}/getSessions",
                verify=False,
                auth=("pxgrid1",secret),
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

