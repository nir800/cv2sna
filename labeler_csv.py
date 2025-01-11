import json
import requests
import getpass
import csv
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings (optional)
warnings.simplefilter('ignore', InsecureRequestWarning)

# Main function to process the CSV and create JSON payloads for PUT requests
def main():
    # Prompt user for username, password, and IP address
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    ip_address = input("Enter the IP address/customer FQDN (e.g., customer-11111111.saas.guardicore.com): ")

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
    
    # Read the CSV file with gc_key, gc_value, and argument (subnet)
    with open('assets.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 3:
                print("Skipping row due to insufficient data:", row)
                continue

            gc_key = row[0].strip()  # Stripping any spaces
            gc_value = row[1].strip()  # Stripping any spaces
            subnet = row[2].strip()  # Stripping any spaces

            # Getting label ID (if required)
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

            # Send request to fetch the label details
            response = requests.get(label_url, headers=headers, params=params, verify=False)
            
            if response.status_code == 200:
                # Debug: Print the full response to inspect its structure
                print(f"Response for gc_key: {gc_key}, gc_value: {gc_value}: {response.text}")
                data = response.json()
                
                # Check if no labels are found
                if not data['objects']:
                    print(f"No labels found for {gc_key} and {gc_value}. Skipping...")
                    continue
                
                try:
                    # Extract label_id from the response
                    label_id = data['objects'][0]['dynamic_criteria'][0]['label_id']
                    print(f"Label ID: {label_id}")
                except (KeyError, IndexError):
                    print(f"Error: Unable to retrieve label ID for {gc_key} and {gc_value}. Response: {data}")
                    continue
            else:
                print(f"Error: {response.status_code} - {response.text}")
                continue

            # Construct criteria for subnets (single subnet for each row)
            criteria = [{
                "op": "SUBNET",
                "field": "numeric_ip_addresses",
                "argument": subnet
            }]

            # Construct URL for PUT request
            url = f"https://{ip_address}/api/v4.0/labels/{label_id}?append=true"

            # Construct the payload with dynamic values
            payload = json.dumps({
                "key": gc_key,
                "value": gc_value,
                "criteria": criteria
            })

            # Send PUT request to update label
            response = requests.put(url, headers=headers, data=payload, verify=False)

            # Check response status
            if response.status_code == 200:
                print(f"Successfully updated label for {gc_key} and {gc_value} with subnet {subnet}")
            else:
                print(f"Failed to update label for {gc_key} and {gc_value} with subnet {subnet}. Status: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    main()
