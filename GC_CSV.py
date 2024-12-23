import csv
import json
import requests


# Read domains from CSV file
def read_domains_from_csv(file_path):
    domains = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            if row:  # Ensure the row is not empty
                domains.append(row[0])
    return domains

# Create JSON payload
def create_payload(domains):
    payload = {
        "action": "ALLOW",
        "destination": {
            "domains": domains
        },
        "enabled": True,
        "ip_protocols": [
            "TCP"
        ],
        "section_position": "ALLOW",
        "source": {
            "address_classification": "Private"
        }
    }
    return json.dumps(payload, indent=2)

# Main function
def main():
    # Authenticate to API
    auth_url = "https://192.168.104.48/api/v3.0/authenticate"
    auth_payload = json.dumps({
        "username": "admin",
        "password": "mainguardicore"
    })
    auth_headers = {
        'Content-Type': 'application/json'
    }
    auth_response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload, verify=False)
    response_data = auth_response.json()
    access_token = response_data.get("access_token")
    print("Access Token:", access_token)

    # Read domains from CSV
    csv_file_path = 'd:\sna\code\domains.csv'  # Update with your CSV file path
    domains = read_domains_from_csv(csv_file_path)
    formatted_domains = [f"*.{domain}" for domain in domains]  # Add *.
    
    # Update policy with domains
    policy_url = "https://192.168.104.48/api/v4.0/visibility/policy/rules/e22d77cf-7d66-4ca4-845c-0c26d2512089"
    policy_payload = create_payload(formatted_domains)
    policy_headers = {
        'Content-Type': 'application/json',
        "authorization": f"Bearer {access_token}"
    }
    policy_response = requests.request("PUT", policy_url, headers=policy_headers, data=policy_payload, verify=False)

    print(policy_response.text)

if __name__ == "__main__":
    main()
