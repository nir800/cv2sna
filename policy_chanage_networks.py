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
    
    # Policy ID input with default value
    policy_id = input("Enter the policy ID (press Enter to use default 'e22d77cf-7d66-4ca4-845c-0c26d2512089'): ")
    if not policy_id:  # If input is empty, use the default policy ID
        policy_id = "e22d77cf-7d66-4ca4-845c-0c26d2512089"

    csv_file_path = 'domainlist.csv'  # Update with your CSV file path
    csv_networks_path = 'networks.csv' #Source ip networks
    domains = read_domains_from_csv(csv_file_path)
    networks= read_domains_from_csv(csv_networks_path)
    
    payload = json.dumps({
        "action": "ALLOW",
        "destination": {
            "domains": domains
        },
        "enabled": True,
        "ip_protocols": [
            "TCP"
        ],
        "ruleset_name": "DomainList",
        "section_position": "ALLOW",
        "source": {
            "subnets": networks
        }
    }, indent=2)

    print("Generated Payload: ", payload)  # Print the payload for verification

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

    # Construct policy URL using the user-provided IP address and policy ID
    policy_url = f"https://{ip_address}/api/v4.0/visibility/policy/rules/{policy_id}"
    policy_headers = {
        'Content-Type': 'application/json',
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # Perform policy update request
        policy_response = requests.put(policy_url, headers=policy_headers, data=payload, verify=False)
        policy_response.raise_for_status()  # Will raise an error for HTTP response codes 4xx/5xx
        
        # Print response from policy update
        print("Policy update response:", policy_response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"Error during policy update request: {e}")
        return

if __name__ == "__main__":
    main()
