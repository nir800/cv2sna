import os
import re
import requests
import json
from time import time
from pprint import pprint
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

######   Setting up the environment ######
ise_user = "admin"
ise_password = "1q2w3e4rT"
base_url = "https://192.168.103.4"  + ":9060/ers/config/"
voucher_group_A = "WhiteList1"
voucher_group_B = "WhiteList2"


auth = HTTPBasicAuth(ise_user, ise_password)
headers = {"Content-Type": "application/json",
           "Accept": "application/json"}



######         ISE functions        ######


def get_ise_group_id(group_name: str):
    '''
    This function will return the ISE group id a given group name.
    '''
    print(f"Fetching for ISE for endpoint group {group_name}...")
    url = base_url + "endpointgroup/name/" + group_name
    response = requests.get(url=url, auth=auth, headers=headers, verify=False)
    if response.status_code == 200:
        group_id = response.json()['EndPointGroup']['id']
        print(f"ISE endpoint group {group_name}, id: {group_id}")
        return(group_id)
    else:
        print(f"\033[1;31mERROR: Group {group_name} was not found\033[0m")
        return("ERROR")


def update_ise_endpoint_group(mac_address: str, group_name: str):
    ise_group_id = get_ise_group_id(group_name)
    print(f"ISE endpoint group name: {group_name}, id: {ise_group_id}")
    if ise_group_id != "ERROR":
        url = base_url + "endpoint/name/" + mac_address
        response = requests.get(
            url=url, auth=auth, headers=headers, verify=False)
        if response.status_code == 200:
            endpoint_id = response.json()["ERSEndPoint"]["id"]
            print(f"ISE endpoint {mac_address}, id: {endpoint_id}")
            # The endpoint exists in the database, need to update its endpoint group assignment
            url = base_url + "endpoint/" + endpoint_id
            data = (
                '{"ERSEndPoint": {"groupId": "%s","staticGroupAssignment": "true"}}' % ise_group_id)
            response = requests.put(
                url=url, data=data, auth=auth, headers=headers, verify=False)
            print(response.json())
            print(f"Response Code Is: {response.status_code}")

            #
        elif response.status_code == 404:
            # The does endpoint exist in the database, need to create it
            # and assign it to the endpoint group
            print(
                f"ISE endpoint {mac_address} was not found. Creating a new one")
            url = base_url + "endpoint/"
            data = {"ERSEndPoint":
                    {
                        "mac": mac_address,
                        "groupId": ise_group_id,
                        "staticGroupAssignment": "true"
                    }
                    }
            response = requests.post(url=url, data=json.dumps(
                data), auth=auth, headers=headers, verify=False)
            print(f"Creation status code: {response.status_code}")
        return("Done")
    else:
        return("ERROR")


def remove_ise_endpoint_group(mac_address: str, group_name: str):
    ise_group_id = get_ise_group_id(group_name)
    if ise_group_id != "ERROR":
        url = base_url + "endpoint/name/" + mac_address
        endpoint_id = requests.get(url=url, auth=auth, headers=headers,
                                   verify=False).json()["ERSEndPoint"]["id"]
        #
        url = base_url + "endpoint/" + endpoint_id
        data = (
            '{"ERSEndPoint": {"groupId": "%s","staticGroupAssignment": "true"}}' % ise_group_id)
        response = requests.delete(
            url=url, data=data, auth=auth, headers=headers, verify=False)
        print(response)
        return("Done")
    else:
        return("ERROR")



# Function to validate a MAC address format
def is_valid_mac_address(mac):
    # The regular expression for a valid MAC address format with colons
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(mac_pattern, mac)

# Prompt the user to input a MAC address
mac_address = input("Enter a MAC address (with colons, e.g., 00:1A:2B:3C:4D:5E): ")

# Check if the input MAC address is valid
if is_valid_mac_address(mac_address):
    print(f"Valid MAC address: {mac_address}")
    
    # Now you can work with the MAC address as needed

    # For example, you can remove colons and convert it to uppercase
    mac_address = mac_address.replace(":", "").upper()
    print(f"MAC address without colons: {mac_address}")
    
    # Or split it into a list of bytes
    mac_bytes = mac_address.split(":")
    print("MAC address bytes:")
    for byte in mac_bytes:
        print(byte)
else:
    print("Invalid MAC address format. Please use the format XX:XX:XX:XX:XX:XX.")


mac=mac_address
voucher_group=voucher_group_A

# # Update ISE
update_ise_endpoint_group(mac, voucher_group)
# # Update ISE
# print(f"Deleting MAC {mac} from ISE")
# remove_ise_endpoint_group(mac_address, voucher_group)
