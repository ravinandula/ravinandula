# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula
# Get the vCenter server thumbprint using the below script

import sys, os, time
import requests, urllib3
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser("This script Get the vCenter Server Thumbprint")

parser.add_argument("--vc-ip", help="Provide the VC IP", required=True)
parser.add_argument("--vc-root-password", help="Provide VC SSO password", required=True)

args = parser.parse_args()

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

		
		
if __name__ == "__main__":
    get_vc_thumbrpint()
