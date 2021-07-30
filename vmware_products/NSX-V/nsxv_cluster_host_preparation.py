# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula
# Get the vCenter server thumbprint using the below script

import argparse, requests

requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser("This script will integrate NSX-V to VC")

parser.add_argument("--vc-ip", help="Provide the VC IP", required=True)
parser.add_argument("--vc-password", help="Provide VC SSO password", required=True)
parser.add_argument("--cluster-name", help="Provide Cluster Name to get the MOID", required=True)
parser.add_argument("--nsxv-ip", help="Provide NSXV IP Address or FQDN", required=True)
parser.add_argument("--nsxv-password", help="Provide NSXV admin password", required=True)


args = parser.parse_args()


def get_vc_session():
    print("Get the VC SESSION ID")
    sessionurl='https://' + args.vc_ip + ':443/rest/com/vmware/cis/session'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}

    r= requests.post(sessionurl, auth=("administrator@vsphere.local", args.vc_password), verify=False, headers=headers)
    if r.status_code == 200:
        return r.json()["value"]
    else:
        print("Unable to get the VC SESSION ID")
        print(r.status_code)
        raise Exception(r.text)

def get_cluster_moid():
    session_id = get_vc_session()
    print("Getting Cluster MOID for the cluster -", args.cluster_name)
    get_cluster_url='https://'+args.vc_ip+'/rest/vcenter/cluster'
    headers = {'content-type': 'application/json',
               'accept': 'application/json'}
    headers["vmware-api-session-id"] = session_id

    r = requests.get(get_cluster_url, verify=False, headers=headers)
    if r.status_code == 200:
        print("Got the Cluster details")
        print(r.text)
        l1 = r.json()["value"]
        for i in l1:
            if i["cluster"] == args.cluster_name:
                print(i["cluster"])
                return i["cluster"]
    else:
        print("Unable to get the Cluster details")
        print(r.text)

def host_prep(cluster_moid):
    print("ESXI Host Preparation")
    host_prep_url='https://'+args.nsxv_ip+'/api/2.0/nwfabric/configure'

    headers = {'Content-Type': 'application/xml'}
    xml = '<?xml version="1.0" encoding="utf-8"?><nwFabricFeatureConfig><resourceConfig><resourceId>'+cluster_moid+'</resourceId></resourceConfig></nwFabricFeatureConfig>'

    r = requests.post(host_prep_url, auth=("admin", args.nsxv_password), data=xml, verify=False, headers=headers)
    if r.status_code == 200:

        print ("Trigger the CLuster HOST Preparation")
        print(r.text)

    else:
        print("Unable to trigger the the Host Preparation")
        raise Exception(r.text)


if __name__ == "__main__":
    cluster_moid=get_cluster_moid()
    host_prep(cluster_moid)