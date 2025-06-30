# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula

import requests
requests.packages.urllib3.disable_warnings()
import argparse


parser = argparse.ArgumentParser("Get Resource Pool Moref")
parser.add_argument("--vc-ip",help="Provide the source vCenter Server IP/FQDN",
                    required=True)
parser.add_argument("--vc-sso-password", help="Provide the VC SSO Password",
                    required=True)
parser.add_argument("--vc-sso-user", help="Provide the VC SSO Username",
                    required=True)
parser.add_argument("--rp-name", help="Provide the Resource Pool",
                    required=True)

args = parser.parse_args()


def get_vc_session(vcip, sso_user, vc_password,):
    print("Get the VC SESSION ID")
    sessionurl = 'https://' + vcip.strip() + ':443/rest/com/vmware/cis/session'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    r = requests.post(sessionurl, auth=(sso_user, vc_password), verify=False, headers=headers)
    if r.status_code == 200:
        return r.json()["value"]
    else:
        print("Unable to get the VC SESSION ID")
        print(r.status_code)
        raise Exception(r.text)


def get_resource_pool_moref(vc_ip, vc_session_id, rp_name):
    print("Get the Resource Pool MOREF")
    rp_url = 'https://'+vc_ip.strip()+'/rest/vcenter/resource-pool'

    headers = {'content-type': 'application/json', 'accept': 'application/json', "vmware-api-session-id": vc_session_id}

    r = requests.get(rp_url, verify=False, headers=headers)
    if r.status_code == 200:
        print("Got the Resource Pool  details")
        print(r.text)
        for i in r.json()["value"]:
            if i["name"] == rp_name:
                print("Moref of the "+rp_name+" RP is - ", i["resource_pool"])
                return i["resource_pool"]
    else:
        print("Unable to get the Cluster details")
        print(r.text)


if __name__ == "__main__":
    vc_session_id = (args.vc_ip, args.vc_sso_user, args.vc_sso_password)
    get_resource_pool_moref(args.vc_ip, vc_session_id, args.rp_name)
