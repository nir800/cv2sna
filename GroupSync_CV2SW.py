
__version__ = "1.1.1.1"
__author__ = "Nir Rephael"
__author_email__ = "nir-r@bynet.co.il"

""" 
Nir Rephael - Bynet Data Communication
Version 1.2 - Stealthwatch dynamic host group, import IPs from Cyber Vision Groups
The script defines functions for validating IPv4 addresses, getting all IP addresses and group names from Cyber Vision 
and updating a SNA host group with a list of IP addresses.
"""


import requests
from urllib3.exceptions import InsecureRequestWarning
import ipaddress
import pandas as pd
import ipaddress
import pandas as pd
import logging
import json
from crayons import blue, red, green
logging.basicConfig(filename="log.log", level=logging.INFO)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

## Login to Cyber Vision ##
center_token = "ics-9505c0fede9afeb87f0820ac7266c2afe13ef4ca-5b81c2c0c1740e925f480e5e398c6f612e2eec71"
center_ip = "192.168.103.49"
center_port = 443
center_base_url = "api/3.0"

## Login to SMC ##
url = "https://192.168.103.16/token/v2/authenticate"

payload = 'username=admin&password=1q2w3e4rT'
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


def is_valid_ipv4_address(address):
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError:
        return False

# Getting all IPs and Group Name


def get_components_ip():
    try:
        headerscv = {"x-token-id": center_token}
        r_get = requests.get(
            f"https://{center_ip}:{center_port}/{center_base_url}/components", headers=headerscv, verify=False)
        r_get.raise_for_status()  # if there are any request errors

        # raw JSON data response
        raw_json_data = r_get.json()

        # get only the label name and IP address of the component
        components_with_ip_and_label = {}
        for component in raw_json_data:
            output = component.get("group")
            if output is not None:
                ip = component.get("ip")
                if is_valid_ipv4_address(ip):
                    components_with_ip_and_label[ip] = output.get("label")
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
    url = "https://192.168.103.16/smc-configuration/rest/v1/tenants/301/tags/"
    payload = {}
    response = requests.request(
        "GET", url, headers=headers, data=payload, verify=False)
    tag_details = json.loads(response.content)["data"]
    for tag in tag_details:
        name = tag["name"]
        id = tag["id"]
        if name == host_group_name:
            return id


# Update Host Group with IP List
def update_IP_hostgorup(id_group, id_name, ip_list):
    url = "https://192.168.103.16/smc-configuration/rest/v1/tenants/301/tags/" + \
        str(id_group)
    payload = {
        "id": id_group,
        "name": id_name,
        "location": "INSIDE",
        "ranges": ip_list,
        "description": "This is sample from Python",
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
    print(blue(f"Done!!!"))

