
__version__ = "1.2"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"

""" 
Nir Rephael - Bynet Data Communication
Version 1.2 - Stealthwatch dynamic host group, import IPs from Cyber Vision Groups
The script defines functions for validating IPv4 addresses, getting all IP addresses and group names from Cyber Vision 
and updating a SNA host group with a list of IP addresses.
"""

from cryptography.fernet import Fernet
import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import ipaddress
import pandas as pd
import ipaddress
import pandas as pd
import logging
import json
import datetime
import pytz
from crayons import blue, red, green
from dotenv import dotenv_values
logging.basicConfig(filename="log.log", level=logging.INFO)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# This is the key to decrypt password 
# tz = pytz.timezone('Asia/Jerusalem')
key = b'oen-jEUBkzcMd7N8fg7z1vTB6iB36qIpaZMqDYjzbe4='
fernet = Fernet(key)

# Import env variables from dotenv file .env 

config = dotenv_values("1.env")

CV_TOKEN = config.get("CV_TOKEN")
CV_IP = config.get("CV_IP")
SMC_IP = config.get("SMC_IP")
SMC_USER = config.get("SMC_USER")
SMC_PASSWORD = config.get("SMC_PASSWORD")
decrypted_data = fernet.decrypt(SMC_PASSWORD)
DECRYPT_SMC_PASSWORD = decrypted_data.decode('utf-8')

# STATIC URLs
SMC_AUTH_URL = '/token/v2/authenticate'
SMC_TAG_URL = '/smc-configuration/rest/v1/tenants/301/tags/'
CV_PORT = 443
CV_BASE_URL = "api/3.0"

## Login to SMC ##
url = f"https://{SMC_IP}{SMC_AUTH_URL}"
payload = 'username=' + SMC_USER + "&" + 'password=' + DECRYPT_SMC_PASSWORD
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request(
    "POST", url, headers=headers, data=payload, verify=False)
## Getting SMC cookies for addtional API calls ##
# print(response.text)
cookies = response.cookies
cookies_dict = requests.utils.dict_from_cookiejar(cookies)
# print(cookies_dict["XSRF-TOKEN"])
# print(cookies_dict["stealthwatch.jwt"])

headers = {
    'Cookie': 'XSRF-Token=' + cookies_dict["XSRF-TOKEN"] + ';' + 'stealthwatch.jwt=' + cookies_dict["stealthwatch.jwt"],
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': cookies_dict["XSRF-TOKEN"]
}

asset_list=[]
def is_valid_ipv4_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

# Getting all IPs and Group Name


def get_components_ip():
    try:
        headerscv = {"x-token-id": CV_TOKEN}
        r_get = requests.get(
            f"https://{CV_IP}:{CV_PORT}/{CV_BASE_URL}/components", headers=headerscv, verify=False)
        r_get.raise_for_status()  # if there are any request errors

        # raw JSON data response
        raw_json_data = r_get.json()
        # with open('data.json', 'w') as file:
        #     json.dump(raw_json_data, file)
        # get only the label name and IP address of the component
        components_with_ip_and_label = {}
        for component in raw_json_data:
            output = component.get("group")
            if output is not None:
                ip = component.get("ip")
                mac = component.get("mac")
                lastActivity = component.get("lastActivity")
                tz = datetime.timezone(datetime.timedelta(hours=3), 'Israel')
                local_time = datetime.datetime.fromtimestamp(lastActivity/1000, tz)
                local_time_short = local_time.strftime('%Y-%m-%d %H:%M:%S')
                id = component.get("id")  
                group= component.get("group")
                label = output.get("label")

                if is_valid_ipv4_address(ip):
                    components_with_ip_and_label[ip] = output.get("label")
                    my_asset_dict = {'ip_addr': ip, 'mac_addr': mac, 'last_activity':local_time_short,'cv_id':id, 'cv_label':label}
                    asset_list.append(my_asset_dict)
 # Create json file for PxGrid Connect as another method pushing context-in
        with open('data.json', 'w') as file:
            asset_list_string=json.dumps(asset_list)
            pxgrid_direct = '{"result":' + asset_list_string + '}'
            file.write(pxgrid_direct)
        file.close    
       
        return components_with_ip_and_label

    except requests.exceptions.HTTPError as e:
        logging.exception(f"HTTP error occurred: {e}")
        return "HTTP error occurred: {}".format(e)
    except requests.exceptions.RequestException as e:
        logging.exception(f"An error occurred: {e}")
        return "An error occurred: {}".format(e)


def get_ip_from_group(group_name: str):
    """
    This function will return the ISE group id a given group name.
    """
    ip = []
    for key, value in all_components.items():
        if value == group_name:
            ip.append(key)

    else:
        return ip


# Getting Group ID from Host Group

 
def get_hostgroup_id(host_group_name: str):
    url=f"https://{SMC_IP}{SMC_TAG_URL}"
    payload = {}
    response = requests.request(
        "GET", url, headers=headers, data=payload, verify=False)
    tag_details = json.loads(response.content)["data"]
    for tag in tag_details:
        name = tag["name"]
        id = tag["id"]
        if name == host_group_name:
            return id

# url = "https://192.168.103.16/smc-configuration/rest/v1/tenants/301/tags/"
# Update Host Group with IP List
def update_IP_hostgorup(id_group, id_name, ip_list):
    
    url=f"https://{SMC_IP}{SMC_TAG_URL}" + \
        str(id_group)
    payload = {
        "id": id_group,
        "name": id_name,
        "location": "INSIDE",
        "ranges": ip_list,
        "description": "Dynmaic update from Python Script",
        "hostBaselines": False,
        "suppressExcludedServices": True,
        "inverseSuppression": False,
        "hostTrap": False,
        "sendToCta": False,
        "domainId": 301,
        "parentId": 1
    }

    response = requests.request(
        "PUT", url, headers=headers, json=payload, verify=False)

    print(response.text)


all_components = get_components_ip()
# Export IP and Group Name to CSV
if isinstance(all_components, dict):
    df = pd.DataFrame(list(all_components.items()), columns=["ip", "label"])
    df.to_csv('nir.csv', index=False)
print(red(all_components))

# List of all Groups in Cyber Vision

my_list = ['MyTestPC', 'Floor1']
def main():
  for group in my_list:
    x = get_ip_from_group(group)
    id_group = get_hostgroup_id(group)
    id_name = group
    print(f"Group Name:{group}: {x}")
    update_IP_hostgorup(id_group, id_name, x)
    print(green(f"Endpoints from Cyber Vision group **{group}** import to SNA host group"))
    

if __name__ == "__main__":
    main()
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Service run: {formatted_time}")
    print(blue(f"\n==>Done!!!  {formatted_time}"))
   

