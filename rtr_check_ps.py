""" This script is using Falcon RTR to run powershell script to bulk computer list.
In example, there is a search for computers running MS defender.
Nir Rephael - Version 1.2
"""
import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning
import json
from crayons import blue, red, green, yellow
from dotenv import dotenv_values
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import os
from falconpy import Hosts, RealTimeResponse, RealTimeResponseAdmin
from argparse import ArgumentParser, RawTextHelpFormatter


# Access to flacon OAuth2 API with client ID and Secrect.
# .env2 file is exclude from github publishing 

config = dotenv_values(".env2")
CLIENT_ID = config.get("client_id")
CLIENT_SECRET = config.get("secret_key")

BOLD = "\033[1m"
NOCOLOR = "\033[0m"

# Below powershell/command input in order to parse a result for each computer from bulk computer list.
# (Get-Process -Name CynetEPS -ErrorAction SilentlyContinue).Name 
COMMAND = "(Get-Process -Name CynetEPS -ErrorAction SilentlyContinue).Name"
TIMEOUT=30
output_file = "output.txt"

# Connect to the CrowdStrike API service collections
hosts = Hosts(client_id=CLIENT_ID,
              client_secret=CLIENT_SECRET
              )
rtr = RealTimeResponse(auth_object=hosts.auth_object)
rtr_admin = RealTimeResponseAdmin(auth_object=hosts.auth_object)
HOST_MATCH=""

def cs_get_info(HOST_MATCH):
    # Retrieve a list of host AIDs that match our search string
    host_ids = hosts.query_devices_by_filter(filter=f"hostname:*'*{HOST_MATCH}*'")
    if host_ids["status_code"] != 200:
        raise SystemExit("Unable to communicate with the CrowdStrike API. Check permissions.")

    if not host_ids["body"]["resources"]:
        raise SystemExit("Unable to find any hosts matching the specified search string.\n"
                        f"Searched for: {BOLD}{HOST_MATCH}{NOCOLOR}"
                        )

    # Retrieve the details for these AIDs so we can lookup the hostnames
    devices = hosts.get_device_details(ids=host_ids["body"]["resources"])["body"]["resources"]

    # Create a mapping dictionary from AID to hostname
    # We'll use this later to display hostnames for results
    device_map = {}
    for device in devices:
        hostname = device.get("hostname", "Not found")
        aid = device.get("device_id", "Not found")
        device_map[aid] = hostname

    print("Starting sessions with target hosts.")
    # Start a batch session with all the hosts we've identified
    session_init = rtr.batch_init_sessions(host_ids=host_ids["body"]["resources"])
    # Create a list to store all of our created session IDs
    session_list = []
    # Retrieve our batch ID
    batch_id = session_init["body"]["batch_id"]
    # Create a list of sessions returned
    sessions = session_init["body"]["resources"]
    # Output successful session connections
    for session in sessions:
        # Grab the ID for this session
        session_id = sessions[session]['session_id']
        # Append this ID to our session list
        session_list.append(session_id)
        print(f"Session with {BOLD}{device_map[session]}{NOCOLOR} started successfully.",
            f"[{session_id}]"
            )

    print(f"\nExecuting command (`{COMMAND}`) against target hosts.\n")
    # Execute our command against the hosts in our batch session
    cloud_request = rtr_admin.batch_admin_command(base_command="runscript",
                                                batch_id=batch_id,
                                                timeout_duration=f"{TIMEOUT}s",
                                                command_string=f"runscript -Raw=```{COMMAND}```"
                                                )

    print("Closing sessions with target hosts.")
    # Close all of our open sessions with these hosts
    for session_id in session_list:
        if rtr.delete_session(session_id=session_id)["status_code"] == 204:
            print(f"Session {BOLD}{session_id}{NOCOLOR} deleted successfully.")
        else:
            print(f"Unable to delete session {BOLD}{session_id}{NOCOLOR}.")

    # Parse and output the results
    if cloud_request["status_code"] == 201:
        results = cloud_request["body"]["combined"]["resources"]
        for result in results:
            print(yellow(f"\n{BOLD}{device_map[result]}"))
            host_name=device_map[result]
            out_data = results[result]
            if out_data["stdout"]:
                lines = out_data["stdout"].strip().split('\n')
                print(f"{host_name}:{lines}")
            
            if out_data["stderr"]:
                print(out_data["stderr"])
            if out_data["errors"]:
                for err in out_data["errors"]:
                    ecode = err["code"]
                    emsg = err["message"]
                    print(f"[{ecode}] {emsg}")
    else:
        # An error occurred
        for err in cloud_request["body"]["errors"]:
            ecode = err["code"]
            emsg = err["message"]
            print(f"[{ecode}] {emsg}")

with open('computers.env', 'r') as file:
    # Iterate through each line in the file
    for line1 in file:
        # Remove leading and trailing whitespace from the line
        HOST_MATCH = line1.strip()
        cs_get_info(HOST_MATCH)
   