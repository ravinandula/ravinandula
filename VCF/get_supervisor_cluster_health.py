# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
import argparse

SUPERVISORY_CLUSTER_URL= "https://{vc_ip}/api/vcenter/namespace-management/clusters/{cluster_id}"


parser = argparse.ArgumentParser("Get the Supervisor Cluster Health")
parser.add_argument("--vc-ip",help="Provide the source vCenter Server IP/FQDN", required=True)
parser.add_argument("--cluster-id", help="Provide the Cluster ID on which the Supervisor is enable",
                    required=True)
parser.add_argument("--session-id", help="Provide the VC session for authentication", required=True)

args = parser.parse_args()


def get_supervisory_cluster_status(session_id, vc_ip, cluster_id):
    headers = {
        "vmware-api-session-id": session_id
    }
    response = requests.get(SUPERVISORY_CLUSTER_URL.format
                                  (vc_ip=vc_ip, cluster_id=cluster_id), headers=headers)

    if response.status_code == 200:
        cluster_response = response.json()
        if (isinstance(cluster_response, dict) and 'value' in cluster_response and
                isinstance(cluster_response['value'], list)):
            if len(cluster_response['value']) != 0:
                for cluster in cluster_response:
                    print(f"Cluster ID: {cluster['cluster']}")
                    print(f"Status: {cluster['config_status']}")
                    print(f"Kubernetes Status:  {cluster['kubernetes_status']}")
                    if (cluster['config_status'] == 'RUNNING'
                            and cluster['kubernetes_status'] == 'READY'):
                        print("Supervisory Cluster Status: RUNNING and its Healthy")
                        return True
                    else:
                        raise Exception("Supervisory Cluster is not in Healthy state")
            else:
                print("SUPERVISORY CLUSTER IS NOT ENABLED")
                raise Exception("SUPERVISORY CLUSTER IS NOT ENABLED, Hence VKS Cluster Creation is not Possible")
    else:
        print(f"Failed to get status. Code: {response.status_code}")
        print(response.text)
        raise Exception(response.text)


if __name__ == "__main__":
    get_supervisory_cluster_status(args.session_id, args.vc_ip, args.cluster_id)