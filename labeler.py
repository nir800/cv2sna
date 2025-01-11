import json
import os
import requests
import getpass

# Main function to test reading CSV and creating JSON list
def main():
    # Prompt user for username, password, IP address, and policy ID
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    ip_address = input("Enter the IP address/customer FQDN (e.g., customer-11111111.saas.guardicore.com): ")
    gc_key = input("Enter key (e.g. Application): ")
    if not gc_key:  # If input is empty, use the default policy ID
           gc_key = "Application"
    gc_value = input("Enter value (e.g. ProjectX): ")
    if not gc_value:  # If input is empty, use the default policy ID
        gc_value = "ProjectX"
    
    

    # Construct authentication URL using the user-provided IP address
    auth_url = f"https://{ip_address}/api/v3.0/authenticate"
    auth_payload = json.dumps({
        "username": username,
        "password": password
    })
    auth_headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Perform authentication request
        auth_response = requests.post(auth_url, headers=auth_headers, data=auth_payload, verify=False)
        auth_response.raise_for_status()  # Will raise an error for HTTP response codes 4xx/5xx
        response_data = auth_response.json()
        
        # Check if the access token is in the response
        access_token = response_data.get("access_token")
        if access_token:
            print("Access Token:", access_token)
        else:
            print("Error: Access token not found in the response.")
            return

    except requests.exceptions.RequestException as e:
        print(f"Error during authentication request: {e}")
        return
    except json.JSONDecodeError:
        print("Error decoding the JSON response from the server.")
        return
    
    
    # getting label ID - No need it for now 
    label_url = f"https://{ip_address}/api/v4.0/labels"
    params = {
        'key': gc_key,
        'value': gc_value
    }
    headers = {
    'Content-Type': 'application/json',
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(label_url, headers=headers, params=params, verify=False)  # verify=False to bypass SSL

    if response.status_code == 200:
        data = response.json()
        print(f"** Data is **: {data}")
        label_id = data['objects'][0]['dynamic_criteria'][0]['label_id']
        print(f"Label ID: {label_id}")
    else:
        print(f"Error: {response.status_code}", response.text)
    

    
    
    url = f"https://{ip_address}/api/v4.0/labels/{label_id}?append=true"


    payload = json.dumps({
    "key": gc_key,
    "value": gc_value,
    "criteria": [
        {
        "op": "SUBNET",
        "field": "numeric_ip_addresses",
        "argument": "10.3.3.0/24"
        },
        {
        "op": "SUBNET",
        "field": "numeric_ip_addresses",
        "argument": "11.4.4.0/24"
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.request("PUT", url, headers=headers, data=payload,verify=False)

    print(response.text)

    
if __name__ == "__main__":
    main()
