import requests
import json

# Load configuration from a config file
def load_config(file_path='config.json'):
    try:
        with open(file_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error parsing JSON in '{file_path}'")
        return {}

# Function to get the access token
def get_access_token(config):
    token_url = config.get("api_url")

    payload = {
        "client_id": config.get("client_id"),
        "client_secret": config.get("client_secret")
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 201:
        response_data = response.json()
        access_token = response_data.get("access_token")
        return access_token
    else:
        print(f"Error: {response.status_code} - Unable to get access token")
        return None

# Function to make the GET request with the access token
def get_detections(api_url, access_token):
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        resources = response_data.get("resources")
        return resources
    else:
        print(f"Error: {response.status_code} - Unable to make GET request")
        return None

# Main function
def main():
    config = load_config()
    if not config:
        return

    access_token = get_access_token(config)
    if access_token:
        api_url = "https://api.crowdstrike.com/detects/queries/detects/v1?limit=1000"
        response_data = get_detections(api_url, access_token)

        if response_data:
            print(json.dumps(response_data, indent=2))

if __name__ == "__main__":
    main() 
        
        



