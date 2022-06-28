import  argparse, base64, time
import requests
requests.packages.urllib3.disable_warnings()



parser = argparse.ArgumentParser("This script will fetch the vRSLCM status after the initial Deployment")


parser.add_argument("--vrslcm-ip", help="Provide the vRSLCM IP", required=True)
parser.add_argument("--lcm-password", help="Provide the vRSLCM password which has to be set for admin@local", required=True)
parser.add_argument("--vidm-nfs-share", help="Provide the DC Name which need to be created in the LCM", required=True)

args = parser.parse_args()


#Get the base64 value for a given password
def get_basic_auth(password):
    print("Getting basic auth value")
    userpass = 'admin@local' + ':' + password
    encoded_u = base64.b64encode(userpass.encode()).decode()

    print("Basic Auth value is", encoded_u)
    return encoded_u

#Map VIDM from NFS
def get_vidm_nfs(vrslcm_ip, basic_auth, vidm_nfs_share):
    print("Fetching the VIDM from NFS")
    vra_nfs = 'https://'+vrslcm_ip.strip()+'/lcm/lcops/api/v2/settings/product-binaries'

    authorization_value = 'Basic ' + basic_auth + ''

    headers = {'Authorization': authorization_value,
               'Content-Type': 'application/json'}


    payload = {
                "sourceLocation": vidm_nfs_share,
                "sourceType": "NFS"
                }

    r = requests.post(vra_nfs, verify=False, headers= headers, json = payload)
    if r.status_code == 200:
        print("Successfully mapped the VIDM from NFS Share")
        print(r.text)
        print("VIDM Name - ", r.json()[0]["name"])
        print("VIDM Filepath - ", r.json()[0]["filePath"])
        return r.json()[0]["name"], r.json()[0]["filePath"]
    else:
        print("Unable to Fetch the VIDM from the NFS")
        raise Exception(r.text)




#Adding VRA Binary to VRSLCM
def add_vidm_binary(vrslcm_ip, basic_auth, vidm_name, vidm_filepath):
    print("#################################")
    print("Adding VRA OVA to VRSLCM binary ")
    print("#################################")
    vra_ova_url = 'https://'+vrslcm_ip.strip()+'/lcm/lcops/api/v2/settings/product-binaries/download'

    authorization_value = 'Basic ' + basic_auth + ''

    headers = {'Authorization': authorization_value,
               'Content-Type': 'application/json'}

    vra_payload = [{"name": vidm_name,
                    "filePath":vidm_filepath,
                    "type":"install"}]

    r = requests.post(vra_ova_url, verify=False, headers= headers, json = vra_payload)

    if r.status_code == 200:
        print("########################################")
        print("Successfully added VIDM OVA to VRSLCM")
        print("########################################")
        print(r.text)
        print(r.json()["requestId"])
        return r.json()["requestId"]
    else:
        print("Unable to add VIDM OVA to VRSLCM ")
        print(r.status_code)
        raise Exception(r.text)

def check_source_mapping_status(vrslcm_ip, basic_auth, request_id):
    print("################################################################")
    print("Fetching the Details for Request ID - ", request_id)
    print("################################################################")

    request_status_url = 'https://'+vrslcm_ip.strip()+'/lcm/request/api/requests/'+request_id.strip()+''

    authorization_value = 'Basic ' + basic_auth + ''

    headers = {'Authorization': authorization_value,
               'Content-Type': 'application/json'}

    while True:
        r = requests.get(request_status_url, headers=headers, verify=False)

        if r.status_code == 200:
            print("Fetched the Request ID status  for -", request_id)
            if r.json()["requestName"] == "sourcemapping":
                if r.json()["state"] == "INPROGRESS":
                    print("Request for Source Mapping is IN-Progress, Hence sleeping for 60 secs")
                    time.sleep(60)
                elif r.json()["state"] == "COMPLETED":
                    print("########################################")
                    print("Request for Source mapping is successful")
                    print("#########################################")
                    break
                elif r.json()["state"] == "CREATED":
                    print("Request for Source Mapping is just CREATED , Hence sleeping for 60 secs")
                    time.sleep(60)
                elif r.json()["state"] == "FAILED":
                    print("Request for Source Mapping FAILED")
                    raise  Exception(r.text)
            else:
                print("This request is not for Source Mapping")
                raise Exception("This request is not for Source Mapping")

        else:
            print("Unable to get the request Status - ")
            raise Exception(r.text)




# main function
if __name__ == "__main__":
    basic_auth= get_basic_auth(args.lcm_password)
    vidm_name, vidm_filepath = get_vidm_nfs(args.vrslcm_ip, basic_auth, args.vidm_nfs_share)
    # Map VIDM in VRSLCM
    vidm_request_id = add_vidm_binary(args.vrslcm_ip, basic_auth, vidm_name, vidm_filepath)

    #Check VIDM Status
    check_source_mapping_status(args.vrslcm_ip, basic_auth, vidm_request_id)

