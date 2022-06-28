import  argparse, base64
import requests
requests.packages.urllib3.disable_warnings()



parser = argparse.ArgumentParser("This script will fetch the vRSLCM status after the initial Deployment")


parser.add_argument("--initial_password", help="Provide the vRSLCM initial password", required=True)
parser.add_argument("--vrslcm-ip", help="Provide the vRSLCM IP", required=True)
parser.add_argument("--lcm-password", help="Provide the vRSLCM password which has to be set for admin@local", required=True)
parser.add_argument("--dc-name", help="Provide the DC Name which need to be created in the LCM", required=True)

args = parser.parse_args()


#Get the base64 value for a given password
def get_basic_auth(password):
    print("Getting basic auth value")
    userpass = 'admin@local' + ':' + password
    encoded_u = base64.b64encode(userpass.encode()).decode()

    print("Basic Auth value is", encoded_u)
    return encoded_u

#Change the Admin password
def set_admin_password(vrslcm_ip, initial_basic_auth, lcm_password):
    print("Setting the VRSLCM admin password")
    password_url = 'https://'+vrslcm_ip.strip( )+'/lcm/authzn/api/firstboot/updatepassword'

    print(password_url)
    authorization_value = 'Basic ' + initial_basic_auth + ''

    headers = {'Authorization': authorization_value,
                'Content-Type': 'application/json'}
    print(headers)

    payload = {"username" :"admin@local" ,"password" :lcm_password}
    print(payload)

    r = requests.put(password_url, verify=False, headers=headers, json=payload)
    if r.status_code == 200:
        print("###############################################")
        print("Successfully updated the vRSLCM admin password")
        print(r.text)
        print("###############################################")

    else:
        print("Unable to change the ADMIN password")
        print(r.status_code)
        raise Exception(r.text)


#Create DC in the VRSLCM
def create_dc(vsrlcm_ip, basic_auth, dc_name):
    print("Creating DC in VRSLCM")
    dc_url = 'https://'+vsrlcm_ip.strip()+'/lcm/lcops/api/v2/datacenters'

    authorization_value = 'Basic ' + basic_auth + ''

    headers = {'Authorization': authorization_value,
               'Content-Type': 'application/json'}

    payload = {
                "dataCenterName": dc_name,
                "primaryLocation": "Bangalore;Karnataka;IN;12.97194;77.59369"
                }

    r = requests.post(dc_url, verify=False, headers= headers, json = payload)
    if r.status_code == 200:
        print("Created DC successfully")
        print("Datacenter ID of UM_DC1 is - ", r.json()["dataCenterVmid"])
        return r.json()["dataCenterVmid"]
    else:
        print("Unable to create DC")
        print(r.status_code)
        raise Exception(r.text)


# main function
if __name__ == "__main__":
    initial_basic_auth = get_basic_auth(args.initial_password)
    set_admin_password(args.vrslcm_ip,initial_basic_auth, args.lcm_password)
    basic_auth = get_basic_auth(args.lcm_password)
    create_dc(args.vrslcm_ip, basic_auth, args.dc_name)

