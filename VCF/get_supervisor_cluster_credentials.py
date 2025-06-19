# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula

import paramiko
import argparse
import re

parser = argparse.ArgumentParser("Get the Supervisor Cluster Credentials")
parser.add_argument("--vc-ip",help="Provide the source vCenter Server IP/FQDN", required=True)
parser.add_argument("--vc-password", help="Provide the VC password", required=True)

args = parser.parse_args()



def get_supervisor_cluster_credentials(vc_ip, vc_password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect
        client.connect(vc_ip, port=22, username="root", password=vc_password)
        print("Connected to vCenter over SSH")

        # Run a command (e.g., list files in /var/log)
        stdin, stdout, stderr = client.exec_command("/usr/lib/vmware-wcp/decryptK8Pwd.py")
        output = stdout.read().decode()
        print("Command Output:\n", output)

        data = ''.join(output)
        ip_match = re.search(r'IP:\s*([\d\.]+)', data)
        pwd_match = re.search(r'PWD:\s*(\S+)', data)
        sv_master_ip = ip_match.group(1) if ip_match else None
        sv_master_pwd = pwd_match.group(1) if pwd_match else None
        print(f"Supervisory Master IP is : {sv_master_ip}")
        print(f"Supervisory Master Password is : {sv_master_pwd}")
        return sv_master_ip, sv_master_pwd
    finally:
        client.close()

if __name__ == "__main__":
    get_supervisor_cluster_credentials(args.vc_ip, args.vc_password)