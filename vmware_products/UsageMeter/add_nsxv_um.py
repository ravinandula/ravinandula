# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula
# Using this script you can add vCenter server and NSX-V to Usagemeter 4.3/4.4



import time, argparse
import requests, urllib3
requests.packages.urllib3.disable_warnings()



parser = argparse.ArgumentParser("This script will add VC and NSX-V to UM")

parser.add_argument("--vc-ip", help="Provide the VC IP", required=True)
parser.add_argument("--vc-sso-username", help="Provide the VC SSO username", required=True)
parser.add_argument("--vc-password", help="Provide VC root password", required=True)
parser.add_argument("--um-ip", help="Provide UM IP", required=True)
parser.add_argument("--um-password", help="Provide UM admin password", required=True)
parser.add_argument("--nsxv-ip", help="Provide NSXV IP Address", required=True)

args = parser.parse_args()


#This fun will generate the session ID for UM
def get_um_session():
    print("Getting the UM session ID")
    authurl='https://'+args.um_ip+':8443/api/v1/login'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}
    payload = {"user": "usagemeter", "password": args.usagemeter_password}
    r = requests.post(authurl, json=payload, verify=False, headers=headers)
    if r.status_code== 202:
        print("Got the UM Session")
        return r.json()['sessionid']
    else:
        print("Unable to create the UM session for the UM {0}".format(args.um_ip))
        raise Exception(r.text)


# Add the deployed VC to UM.
def add_vc(session_id):
    url='https://'+args.um_ip+'/api/v1/product'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    headers["sessionId"] = session_id
    payload = {"productType": "vCenter", "externalSSO": False, "srmMetered": True,
               	"user": args.vc_sso_username, "password": args.vc_sso_password, "vcfEdition": "None",
               	"tanzuEdition": "Basic", "k8sMetric": "vRAM","host": ''+args.vc_ip+'', "port": 443}
    print(payload)
    r = requests.post(url, json=payload, verify=False, headers=headers)
    if r.status_code == 202:
        print("Added VC to UM , Please accept the certificate")
        vc_product_id=r.json()["id"]
        print("Product ID is "+ str(vc_product_id))
        time.sleep(20)
        accepturl='https://'+args.um_ip+'/api/v1/accept_certificate'
        headers = {'content-type': 'application/json',
                   'accept': 'application/json'}
        headers["sessionId"] = session_id
        acceptpayload={"productType": "vCenter", "productId": vc_product_id,
                       "certificateId": ''+args.vc_ip+':443', "accepted": "true"}
        ar=requests.put(accepturl, json=acceptpayload, verify=False, headers=headers)
        if ar.status_code == 202:
            print("Accepeted the VC certificate SUCCESSFULLY")
            #print(ar.text)
            return vc_product_id
        else:
            print("Unable to Accept the Certificate")
            print(ar.status_code)
            raise Exception(ar.text)
    else:
        print("Unable to Add VC to UM")
        print(r.status_code)
        raise Exception(r.text)

def add_nsxv(session_id,vc_id):
    print("Adding the NSX-V to UM")
    nsxv_url='https://'+args.um_ip+'/api/v1/product'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    headers["sessionId"] = session_id
    payload={"productType": "NSX-V","user": "admin","password": args.nsxv_password,"vcId": vc_id,"host": args.nsxv_ip,"port": 443}

    print(payload)
    r = requests.post(nsxv_url, json=payload, verify=False, headers=headers)
    if r.status_code == 202:
        print("Added NSX-V to UM , Please accept the certificate")
        nsxv_product_id=r.json()["id"]
        print("Product ID is "+ str(nsxv_product_id))
        time.sleep(20)
        accepturl='https://'+args.um_ip+'/api/v1/accept_certificate'
        headers = {'content-type': 'application/json',
                   'accept': 'application/json'}
        headers["sessionId"] = session_id
        acceptpayload={"productType": "NSX-V", "productId": nsxv_product_id,
                       "certificateId": ''+args.nsxv_ip+':443', "accepted": "true"}
        ar=requests.put(accepturl, json=acceptpayload, verify=False, headers=headers)
        if ar.status_code == 202:
            print("Accepeted the VC certificate SUCCESSFULLY")
            #print(ar.text)
        else:
            print("Unable to Accept the Certificate")
            print(ar.status_code)
            raise Exception(ar.text)
    else:
        print("Unable to Add VC to UM")
        print(r.status_code)
        raise Exception(r.text)


if __name__ == "__main__":
    session_id = get_um_session()
    print("Adding Newly Deployed VC to UM")
    vc_product_id=add_vc(session_id)
    print("#####################################################")
    add_nsxv(session_id,vc_product_id)