# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula

import argparse
import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

parser = argparse.ArgumentParser()
parser.add_argument("--vcIP",help="Provide the source vCenter Server IP/FQDN", required=True)
parser.add_argument("--nsxtIP", help="Provide the NSXT IP/FQDN", required=True)
parser.add_argument("--nsxtUser", help="Provide the NSXT Username", required=True)
parser.add_argument("--nsxtPassword", help="Provide the NSXT Password ", required=True)
parser.add_argument("--vcThumprint", help="Provide the VC thumbprint ", required=True)
parser.add_argument("--vcUsername", help="Provide the VC SSO Username ", required=True)
parser.add_argument("--vcPassword", help="Provide the VC SSO Password ", required=True)
parser.add_argument("--transportZoneName", help="Provide the TransportZone Name ", default="ravi-tz1", required=False)

args = parser.parse_args()

COMPUTE_MANAGER_URL = 'https://'+ args.nsxtIP +'/api/v1/fabric/compute-managers'
TRANSPORT_ZONE_URL = 'https://'+ args.nsxtIP +'/api/v1/transport-zones/'

#This function will get the existing Compute Manager details from NSX-T
def getComputeManager():
    print  "Get the details of Existing Compute Managers in the NSX-T"
    print "Running the following URL :" +COMPUTE_MANAGER_URL
    r= requests.get(COMPUTE_MANAGER_URL, auth=(args.nsxtUser, args.nsxtPassword), verify=False)
    if r.status_code == 200:
        printr.text
        print "Able to Get the Existing Compute Managers"
    else:
        print "Looks like NSX is UP and running, Could not get the Existing Compute Manager details"
        print r.status_code
        raise Exception(r.text)

#This function will create a new Compute Manager in NSX-T
def createComputeManager():
    print "####################################################"
    print "Creating the Compute Managers in the NSX-T"
    print "Running the following API Call" +COMPUTE_MANAGER_URL
    headers = {'content-type': 'application/json'}
    payload = {"server": args.vcIP, "origin_type": "vCenter"}
    payload["credential"]= {"credential_type" : "UsernamePasswordLoginCredential",  "username": args.vcUsername, "password": args.vcPassword, "thumbprint": args.vcThumprint }
    print payload
    r = requests.post(COMPUTE_MANAGER_URL, verify=False, auth=(args.nsxtUser, args.nsxtPassword), json=payload, headers=headers)
    if r.status_code == 201:
        print r.text
        print "Successfully added VC to Compute Manager "
    else:
        print  "Unable to add VC to Compute Manager , Please login to NSX-T and verify"
        print r.status_code
        raise Exception(r.text)

#This function will create a Transport Zone in the NSX-T
def createTransportZone():
    print "####################################################"
    print "Creating the Transport Zone in the NSX-T"
    print "Running the following API Call" + TRANSPORT_ZONE_URL
    headers = {'content-type': 'application/json'}
    payload = {"display_name": args.transportZoneName, "host_switch_name": "vDS",  "description": "Transport Zone 1", "transport_type": "OVERLAY" }
    print payload
    r =  requests.post(TRANSPORT_ZONE_URL, verify=False, auth=(args.nsxtUser, args.nsxtPassword), headers=headers, json=payload)
    if r.status_code == 201:
        print r.text
        print "Successfully created Transport Zone"
    else:
        print "Unable to create the transport zone. Please check the below error and correct it"
        print r.status_code
        raise Exception(r.text)


def main():
    exit_code = 0
    try:
        getComputeManager()
        createComputeManager()
        createTransportZone()
    
    raise Exception as e:
        print e
        exit_code = 1
    finally:
        sys.exit(exit_code)

if __name__ == "__main__":
        main()

