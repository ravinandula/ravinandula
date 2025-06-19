import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
import argparse



parser = argparse.ArgumentParser("Create Namespace")
parser.add_argument("--vc-ip",help="Provide the source vCenter Server IP/FQDN", required=True)
parser.add_argument("--vc-session-id", help="Provide the VC Session ID", required=True)
parser.add_argument("--cluster-name", help="Provide the Cluster Name", required=True)
parser.add_argument("--vc-ns", help="Provide the Namespace Name", required=True)


args = parser.parse_args()

GET_CLUSTER_ID_URL = "https://{vc_ip}/rest/vcenter/cluster"
GET_STORAGE_POLICIES_URL = "https://{vc_ip}/api/vcenter/storage/policies"
STORAGE_POLICY_PREFIX= "wcp"
CREATE_NAMESPACE_URL = "https://{vc_ip}/api/vcenter/namespaces/instances"

#Get the CLuster ID on which supervisor is Activated
def get_cluster_id(cluster_name, session_id, vc_ip):
    headers = {"vmware-api-session-id": session_id}


    response = requests.get( GET_CLUSTER_ID_URL.format(vc_ip=vc_ip),
                             headers=headers)
    if response.status_code == 200:
        for cluster in response.json()["value"]:
            if cluster["name"] == cluster_name:
                print(f"CLuster ID is - {cluster['cluster']}")
                return cluster["cluster"]
    else:
        raise Exception("Cluster does not exists")

#Get the Storage Policy ID
def get_storage_policy_id(session_id, vc_ip):

        headers = {"vmware-api-session-id": session_id}


        response = requests.get(GET_STORAGE_POLICIES_URL.format(vc_ip=vc_ip),
                                headers=headers)

        if response.status_code == 200:
            policy_list = response.json()
            for policy in policy_list:
                if policy['name'].startswith(STORAGE_POLICY_PREFIX):
                    print(f"Policy Name -{policy['name']} =>Policy ID - {policy['policy']}")
                    return policy['policy'], policy['name']
            return "NOT_FOUND"
        else:
            raise Exception(response.text)

#Create Namespace
def create_namespace_in_sup(session_id, cluster_id, storage_policy_id, vc_ip, vc_ns):

    headers = {
        "vmware-api-session-id": session_id,
        "Content-Type": "application/json"
    }

    payload = {
        "cluster": cluster_id,
        "namespace": vc_ns,
        "description": "Namespace for Dev Team",
        "network_spec": {
            "network": "dvportgroup-21"
        },
        "storage_specs":
            [
                {
                    "policy": storage_policy_id,
                    "default": True
                }
            ],
        "vm_service_spec": {
            "vm_classes": [
                "best-effort-xsmall"
            ]
        }
    }


    response = requests.post(CREATE_NAMESPACE_URL.format(vc_ip=vc_ip),
                                   headers=headers, data=payload)

    print(response)

    if response.status_code == 204:
        print("Namespace created successfully!")
        print(f"Response Text is {response.text}")
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)
        raise Exception(response.text)



def main():
    cluster_id = get_cluster_id(args.cluster_name, args.cluster_session_id, args.vc_ip)
    storage_policy_id = get_storage_policy_id(args.session_id, args.vc_ip)
    create_namespace_in_sup(args.session_id, cluster_id, storage_policy_id, args.vc_ip, args.vc_ns)

if __name__ == "__main__":
    main()
