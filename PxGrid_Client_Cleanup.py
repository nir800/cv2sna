# Nir Rephael
# Account Approved. Password is T4u78yj1A2jcLPnh
# Websocket (using STOMP) to PxGrid without RestAPI polling 
import json
import requests
import ssl
import websocket
import re
import mab_cleanup
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
     # print(my_string)
     match = re.search(r'{.*}', my_string)
     
     if match:
        json_str = match.group(0)
        json_obj = json.loads(json_str)
        #print(json_obj)
        print(blue(json_obj))  
        #state_value = json_obj['sessions'][0]['state']
        #print(state_value)
        state = json_obj['sessions'][0]['state']
        mac_address = json_obj['sessions'][0]['macAddress']
        endpoint_profile = json_obj['sessions'][0]['endpointProfile']
        #### send to delete mac function delete_mac, 
        #### args=(mac, cleanup_groups, endpoint_profile )
              

        # Print the values
        print(green(f"\n==>State is:{state}"))
        print(green(f"\n==>MAC is:{mac_address}"))
        print(green(f"\n==>Endpoint Profile is:{endpoint_profile}"))
        
        # print('State:', state)
        # print('MAC Address:', mac_address)
        # print('Endpoint Profile:', endpoint_profile)
        if state=="DISCONNECTED":
            #test_mac(mac_address,endpoint_profile)
            delete_mac(mac_address,cleanup_groups)
     else:
        print('No JSON substring found in input string.')

 
        
    
    
def on_error(wsapp,error):
    print(f"Websocket error: {error}")
    
def test_mac(mac: str, cleanup_groups: list):
    print("My MAC is" + mac + "My Group is:" + cleanup_groups)
    
def delete_mac(mac: str, cleanup_groups: list):
    endpoint_id, endpoint_group_id = mab_cleanup.get_endpoint_by_mac(mac)
    print(f"Endpoint ID for MAC {mac} is: {endpoint_id}, Group ID is: {endpoint_group_id}")
    if cleanup_groups == [] or endpoint_group_id in cleanup_groups:
        print ("We can delete the MAC from:" + endpoint_group_id )
        mab_cleanup.delete_endpoint(endpoint_id)
    else:
        print(f"Group {endpoint_group_id} is not in the cleanup group list. Ignoring.")
    
if __name__ == "__main__":
    # cleanup groups are list of groups id for cleanup 
    cleanup_groups = mab_cleanup.get_ise_cleanup_groups()
    if cleanup_groups == "ERROR" or cleanup_groups == []:
        print("No filter found - cleaning all endpoint groups.")
        cleanup_groups = []


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



# import websocket
# import ssl
# from base64 import b64encode

# def on_message(ws, message):
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws):
#     print("### WebSocket connection closed ###")

# def on_open(ws):
#     ws.send('{"topic":"com.cisco.ise.radius","messageType":"EIS_MESSAGE","payloadFormat":"JSON","payload":{"destinationIP":"192.168.103.51","destinationPort":1812,"userName":"nir","callingStationId":"34:E6:D7:70:13:90","serviceName":"dot1x","protocol":"EAP-FAST (EAP-MSCHAPv2,EAP-TLS)","sessionID":"C0A8673300000574B1846908","authenticationMethod":"dot1x","stepName":"STEP_1","stepMessage":"Evaluating Identity Policy"}}')

# if __name__ == "__main__":
#     secret = "your_secret"
#     ws_url = "wss://192.168.103.51:8910/pxgrid"
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE
#     header = {"Authorization": "Basic "+b64encode((f"pxgridnir:{secret}").encode()).decode()}
#     wsapp = websocket.WebSocketApp(
#         ws_url,
#         header=header,
#         on_open=on_open,
#         on_message=on_message,
#         on_error=on_error,
#         on_close=on_close,
#         sslopt={"context": ssl_context},
#     )

#     try:
#         wsapp.run_forever()
#     except KeyboardInterrupt:
#         wsapp.close()





