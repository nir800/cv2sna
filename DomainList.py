import csv
import json
import os
import requests
import getpass
import keyboard

# This is for ***** password
def input_password(prompt):
    print(prompt, end="", flush=True)
    password = []
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'enter':
                break
            elif event.name == 'backspace':
                if password:
                    password.pop()
                    print('\b \b', end="", flush=True)  # Erase last character
            else:
                password.append(event.name)
                print('*', end="", flush=True)  # Display * for each character
    print()  # Move to the next line
    return ''.join(password)

# password1 = input_password("Enter your password: ")
# print("Password entered successfully."+ password1)

# Read domains from CSV file and create JSON list
def read_domains_from_csv(file_path):
    domains = []
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return ["example.com"]

    with open(file_path, 'r') as file:
        content = file.read()
        print(f"CSV File Content:\n{content}")  # Debugging to check file content
        file.seek(0)  # Reset file pointer
        reader = csv.reader(file)
        for row in reader:
            print(f"Row: {row}")  # Debugging to check CSV rows
            # Handle both single row CSV (comma-separated) and multi-row
            for cell in row:
                domains.extend([domain.strip() for domain in cell.split(',') if domain.strip()])
    print(f"Collected Domains: {domains}")  # Debugging to check collected domains
    return domains if domains else ["example.com"]  # Default if empty

# Main function to test reading CSV and creating JSON list
def main():
    csv_file_path = 'domains.csv'  # Update with your CSV file path
    domains = read_domains_from_csv(csv_file_path)
    
    payload = json.dumps({
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
    }, indent=2)

    print(payload)  # Print the payload for verification

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

    policy_url = "https://192.168.104.48/api/v4.0/visibility/policy/rules/e22d77cf-7d66-4ca4-845c-0c26d2512089"
    policy_headers = {
        'Content-Type': 'application/json',
        "authorization": f"Bearer {access_token}"
    }
    policy_response = requests.request("PUT", policy_url, headers=policy_headers, data=payload, verify=False)

    print(policy_response.text)
    
if __name__ == "__main__":
    main()
