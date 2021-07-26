# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula
# Get the vCenter server thumbprint using the below script

import subprocess
import json, sys, time
import paramiko


parser = argparse.ArgumentParser("This script Get the vCenter Server Thumbprint")

parser.add_argument("--vc-ip", help="Provide the VC IP", required=True)
parser.add_argument("--vc-password", help="Provide VC SSO password", required=True)
parser.add_argument("--nsxv-ip", help="Provide NSXV IP Address or FQDN", required=True)

args = parser.parse_args()

def reg_nsxv(vc_thumbprint):
    print()
    reg_url='https://'+args.nsxv_ip+'/api/2.0/services/vcconfig'
    headers = {'Content-Type': 'application/xml'}
    payload = {"ipAddress": args.vc_ip,"userName": "administrator@vsphere.local","password": args.vc_password,
               "certificateThumbprint": vc_thumbprint,
               "assignRoleToUser": [], "pluginDownloadServer": [],"pluginDownloadPort": []}


    r = requests.put(reg_url, json=payload, verify=False, headers=headers)
    if r.status_code == 400:
        print("Got 400 Invalid response")
        print(r.text)
        actual_thumbprint=r.json()["details"]
        print("Actual Thumbprint is ", actual_thumbprint)
        payload1={"ipAddress": args.vc_ip,"userName": "administrator@vsphere.local","password": args.vc_password,
               "certificateThumbprint": actual_thumbprint,
               "assignRoleToUser": [], "pluginDownloadServer": [],"pluginDownloadPort": []}
        s = requests.put(reg_url, json=payload, verify=False, headers=headers)
        if s.status_code ==200:
            print("NSX-V is integrated to VC")
            print(s.text)
        else:
            print (s.status_code)
            print (s.text)
			raise Exception(s.text)



def get_vc_thumbrpint():
    print("#######################################################")
    print("Getting the vCenter server Thumbprint for -",args.vc_ip)
    print("#######################################################")
    if vc_ip:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        count = 1
        while True:
            print("Trying to establish connection, Try:" ,count)
            try:
                print('Making connection to '+args.vc_ip+', using root credentails ')
                ssh.connect(args.vc_ip, username='root', password=args.vc_root_password)
                print("Test connecting to SSH Agent successful")
                break
            except Exception as e:
                print("Error in connection, retrying")
                print(e)
                time.sleep(30)
                count = count + 1
                if count >= 3:
                    print("Test connecting to the SSH Agent failed")
                    sys.exit(-1)
        print("Connected to vCenter server")
        command= 'openssl x509 -in /etc/vmware-vpx/ssl/rui.crt -fingerprint -sha1 -noout'
        status, stdout, stderr = update_um_event_gateway.issue_command(ssh.get_transport(), 1,
                                                                       command)


        words=stdout.split("=")
		print("VC Thumbprint is - ",words[1])
		return words[1]
			
		
if __name__ == "__main__":
    vc_thumbprint=get_vc_thumbrpint()
	reg_nsxv(vc_thumbprint)