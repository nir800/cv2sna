import requests
import json

url = "https://192.168.104.48/api/v3.0/authenticate"

payload = json.dumps({
  "username": "admin",
  "password": "mainguardicore"
})
headers = {
  'Content-Type': 'application/json',
  
}

response = requests.request("POST", url, headers=headers, data=payload,verify=False)

response_data = response.json()
access_token = response_data.get("access_token")
print("Access Token:", access_token)


url = "https://192.168.104.48/api/v4.0/visibility/policy/rules/e22d77cf-7d66-4ca4-845c-0c26d2512089"

payload = json.dumps({
  "action": "ALLOW",
  "destination": {
    "domains": [
      "*.ynet.com",
      "*.google.com",
      "*.bynet.co.il",
      "*.migdal.co.il"
    ]
  },
  "enabled": True,
  "ip_protocols": [
    "TCP"
  ],
  "section_position": "ALLOW",
  "source": {
    "address_classification": "Private"
  }
})
headers = {
  'Content-Type': 'application/json',
  "authorization": f"Bearer {access_token}"
}

response = requests.request("PUT", url, headers=headers, data=payload,verify=False)

print(response.text)

