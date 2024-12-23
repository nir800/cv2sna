import requests
import json

# First Request - Authenticate
url = "https://192.168.104.48/api/v3.0/authenticate"

payload = json.dumps({
  "username": "admin",
  "password": "mainguardicore"
})

headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

response_data = response.json()
access_token = response_data.get("access_token")

if access_token:
    print("Access Token:", access_token)
else:
    print("Authentication failed.")
    exit(1)

# Second Request - Policy Revision Update
rurl = "https://192.168.104.48/api/v4.0/visibility/policy/revisions"

payload = json.dumps({
  "ruleset_name": "DomainList",  # Use regular quotes
  "comments": "Update Domain List",  # Properly closed quote and string
  "reset_hit_count": False  # Python uses False, but it will be serialized to `false` in JSON
})

headers = {
    'Content-Type': 'application/json',
    "Authorization": f"Bearer {access_token}"
}

response = requests.request("POST", rurl, headers=headers, data=payload, verify=False)

print(response.text)
