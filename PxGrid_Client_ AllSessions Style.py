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
from rich import print as pp
from rich.console import Console
from rich.table import Table
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

# Create a console object for rich output
console = Console()

for session in sessions:
    timestamp = session['timestamp']
    state = session['state']
    userName = session['userName']
    nasPortId = session['nasPortId']
    ipAddresses = session['ipAddresses'][0]
    count=count+1
  # Print session details with rich formatting
    console.print(f"[bold]Session {count}:")
    console.print(f"Timestamp: [bold]{timestamp}[/bold]")
    console.print(f"State: [bold]{state}[/bold]")
    console.print(f"UserName: [bold]{userName}[/bold]")
    console.print(f"nasPortId: [bold]{nasPortId}[/bold]")
    console.print(f"IP Address: [bold]{ipAddresses}[/bold]")
    console.print()
  
print(red(f"Number of actvice endpoints:{count}"))

# Create a table object for rich output
table = Table(title="Session Details")
table.add_column("Session", style="bold")
table.add_column("Timestamp")
table.add_column("State")
table.add_column("UserName")
table.add_column("nasPortId")
table.add_column("IP Address")

for count, session in enumerate(sessions, start=1):
    timestamp = session['timestamp']
    state = session['state']
    userName = session['userName']
    nasPortId = session['nasPortId']
    ipAddresses = session['ipAddresses'][0]
    
    # Add session details to the table
    table.add_row(
        str(count),
        timestamp,
        state,
        userName,
        nasPortId,
        ipAddresses
    )

# Print the table
pp(table)





