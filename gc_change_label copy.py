import csv
import json
import os
import requests
import getpass


# Read domains from CSV file and create JSON list
def read_domains_from_csv(file_path):
    domains = []
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return ["example.com"]  # Default value if the file doesn't exist
    
    # Open the file with utf-8-sig encoding to handle BOM properly
    with open(file_path, 'r', encoding='utf-8-sig', newline='') as file:
        content = file.read()  # Read all content for debugging
        print(f"CSV File Content:\n{content}")  # Debugging to check file content

        # Reset file pointer for proper CSV reading
        file.seek(0)
        reader = csv.reader(file)
        
        for row in reader:
            for cell in row:
                # Strip unwanted characters (including BOM if present)
                domain = cell.strip()
                # Add the cleaned domain to the list
                domains.append(domain)
    
    # If no domains are found, return the default example
    return domains if domains else ["example.com"]



# Main function to test reading CSV and creating JSON list
def main():
    # Prompt user for username, password, IP address, and policy ID
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    ip_address = input("Enter the IP address/customer FQDN (e.g., customer-11111111.saas.guardicore.com): ")
   

    csv_file_dst = 'destinations.csv'  # Update with your CSV file path
    # csv_networks_source = 'sources.csv' #Source ip networks
    destinations = read_domains_from_csv(csv_file_dst)
    
    

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
        'key': 'Application',
        'value': 'ProjectX'
    }
    headers = {
    'Content-Type': 'application/json',
    "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(label_url, headers=headers, params=params, verify=False)  # verify=False to bypass SSL

    
    if response.status_code == 200:
        data = response.json()
        print(data)
        label_id = data.get('objects', [{}])[0].get('id')
        print(f"ID: {label_id}")
    else:
        print(f"Error: {response.status_code}", response.text)


    
    url = "https://192.168.104.48/api/v4.0/labels/f64358b1-4eb7-45f0-97db-ee7a5f74e888"
    params = {
        'append': 'true'
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "value": "ProjectX",
        "criteria": [
            {
                "field": "numeric_ip_addresses",
                "op": "SUBNET",
                "argument": "10.1.1.0/24"
            }
        ],
        "key": "Role"
    }

    response = requests.put(url, headers=headers, params=params, data=json.dumps(data), verify=False)  # verify=False to bypass SSL

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code}", response.text)


    ## Update network/subnet to label with  
    # update_label_url = f"https://{ip_address}/api/v4.0/labels/Application/ProjectX/subnets"
    
    # headers = {
    #       'accept': 'application/json',
    #       'Content-Type': 'application/json',
    #       "Authorization": f"Bearer {access_token}"
    # }
    # data = [
    #         {"subnet": "1.1.1.1"}
    #     ]

    # response = requests.post(update_label_url, headers=headers, data=json.dumps(data), verify=False)  # verify=False to bypass SSL

    # if response.status_code == 200:
    #         print(response.json())
    # else:
    #         print(f"Error: {response.status_code}", response.text)

if __name__ == "__main__":
    main()
