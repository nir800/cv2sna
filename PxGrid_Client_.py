# Nir Rephael
# Account Approved. Password is T4u78yj1A2jcLPnh
# Websocket (using STOMP) to PxGrid without RestAPI polling 
import json
import requests
import ssl
import websocket
import re
import mab_cleanup
import datetime
from crayons import blue, red, green
from base64 import b64encode
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
password = "T4u78yj1A2jcLPnh"
# Pxgrid client name is pxgridnir, so you need to change it if name is diffrent on
# all the lines
# pip install websocket-client for websock module

# Service Lookup
r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/ServiceLookup",
                verify=False,
                auth=("pxgridnir",password),
                json={"name":"com.cisco.ise.session"})       
r.raise_for_status()
json_response=r.json()
#print(json.dumps(json_response,indent=2))
service_info=r.json()["services"][0]
session_topic=service_info["properties"]["sessionTopic"]
pubsub_service=service_info["properties"]["wsPubsubService"]



# Service lookup for pubsub, getting wsURL 
r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/ServiceLookup",
                verify=False,
                auth=("pxgridnir",password),
                json={"name":pubsub_service})       
r.raise_for_status()
json_response=r.json()
#print(json.dumps(json_response,indent=2))
service_info=r.json()["services"][0]
node_name=service_info["nodeName"]
ws_url=service_info["properties"]["wsUrl"]

 
#  "nodeName": "~ise-pubsub-ise32",
#  "wsUrl": "wss://ise32.cyber.lab:8910/pxgrid/ise/pubsub"

# Access to node secret (different from the password we are using for authentication)

r=requests.post("https://ise32.cyber.lab:8910/pxgrid/control/AccessSecret",
                verify=False,
                auth=("pxgridnir",password),
                json={"peerNodeName":node_name})       
r.raise_for_status()
json_response=r.json()
#print(json.dumps(json_response,indent=2))
secret=r.json()["secret"]
#print(f"password is: {secret}")



# Next Steps
# Establish WebSocket Connection, send STOMP Connect, send STOMP Subscribe
# Need to send binary commands and not text, using 2 callbacks for connection and for messages 

def on_open(wsapp):
    wsapp.send(f"CONNECT\naccept-version:1.2\nhost:{node_name}\n\n\x00",websocket.ABNF.OPCODE_BINARY)
    wsapp.send(f"SUBSCRIBE\ndestination:{session_topic}\nid:nir\n\n\x00",websocket.ABNF.OPCODE_BINARY)

def on_message(wsapp,message):
       
    my_string = message.decode()
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(red(f"Time is: {formatted_time}"))
    print(green(f"{my_string}"))
    print(red(f"========================================================================================================="))
                
              
 
        
    
    
def on_error(wsapp,error):
    print(f"Websocket error: {error}")
    

    
if __name__ == "__main__":
  

    ssl_context=ssl.create_default_context()
    # ssl_context.load_verify_locations(cafile="root.cer")
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    header = {"Authorization": "Basic "+b64encode((f"pxgridnir:{secret}").encode()).decode()}
    wsapp=websocket.WebSocketApp(ws_url, header=header, on_open=on_open, on_message=on_message, on_error=on_error)
    try:
        print("press Ctrl+C to close the WebSocket connection ")
        wsapp.run_forever(sslopt={"context": ssl_context})
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Websocket Closed!!!!")
        wsapp.close()


