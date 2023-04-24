# This script is for creating pxgrid client based on password.
# There is a need to save the password for more pxgrid API calls.
import json
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/AccountCreate",
                     verify=False,
                     json={"nodeName": "pxgridnir"})
    r.raise_for_status()
    password=r.json()["password"]
    while True:
        r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/AccountActivate",
                         verify=False,
                         auth=("pxgridnir",password),
                         json={})       
        r.raise_for_status()
        json_response=r.json()
        print(json.dumps(json_response,indent=2))
        if json_response["accountState"]=="ENABLED":
            print(f"Account Approved. Password is {password}")
            break
        sleep(60)
except requests.exceptions.RequestException as e:
    print(e)
