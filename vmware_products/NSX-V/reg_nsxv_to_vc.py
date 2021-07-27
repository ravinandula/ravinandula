# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula
# Get the vCenter server thumbprint using the below script

import subprocess
import json, sys, time
import paramiko
import requests

parser = argparse.ArgumentParser("This script will integrate NSX-V to VC")

parser.add_argument("--vc-ip", help="Provide the VC IP", required=True)
parser.add_argument("--vc-password", help="Provide VC SSO password", required=True)
parser.add_argument("--nsxv-ip", help="Provide NSXV IP Address or FQDN", required=True)
parser.add_argument("--nsxv-password", help="Provide NSXV admin password", required=True)
parser.add_argument("--vc-root-password", help="Provide NSXV admin password", required=True)

args = parser.parse_args()


def reg_nsxv(vc_thumbprint):
    print("Running NSXV Reg API")
    reg_url='https://'+args.nsxv_ip+'/api/2.0/services/vcconfig'
    print(reg_url)
    headers = {'Content-Type': 'application/xml'}
    xml='<?xml version="1.0" encoding="utf-8"?><vcInfo><ipAddress>'+args.vc_ip+'</ipAddress>' \
            '<userName>administrator@vsphere.local</userName><password>'+args.vc_password+'</password><certificateThumbprint>'+vc_thumbprint+'' \
            '</certificateThumbprint><assignRoleToUser></assignRoleToUser><pluginDownloadServer></pluginDownloadServer>' \
            '<pluginDownloadPort></pluginDownloadPort></vcInfo>'


    r = requests.put(reg_url,auth=("admin", args.nsxv_password), data=xml, verify=False, headers=headers)
    if r.status_code == 400:
        print("Got 400 Invalid response")
        print(r.text)
        actual_thumbprint=r.json()["details"]
        print("Actual Thumbprint is ", actual_thumbprint)
        new_xml = '<?xml version="1.0" encoding="utf-8"?><vcInfo><ipAddress>' + args.vc_ip + '</ipAddress>' \
             '<userName>administrator@vsphere.local</userName><password>'+args.vc_password+'</password><certificateThumbprint>' + actual_thumbprint+ '' \
            '</certificateThumbprint><assignRoleToUser></assignRoleToUser><pluginDownloadServer></pluginDownloadServer>' \
             '<pluginDownloadPort></pluginDownloadPort></vcInfo>'


        s = requests.put(reg_url,auth=("admin", args.nsxv_password), data=new_xml, verify=False, headers=headers)
        if s.status_code ==200:
            print("NSX-V is integrated to VC")
            print(s.text)
        else:
            print (s.status_code)
            print (s.text)
    else:
        print(r.status_code)
        print(r.text)

def issue_command(transport, pause, command):
        print("Executing" + command)
        chan = None
        retryCount = 10
        while retryCount >= 0:
            retryCount = retryCount - 1
            try:
                chan = transport.open_session()
                break
            except:
                print("Got exception while opening session. Will retry...")
                time.sleep(5)
                continue
        if chan == None:
            raise Exception("Got Channel as None. Quiting...")
        chan.exec_command(command)

        buff_size = 1024
        stdout = ""
        stderr = ""

        while not chan.exit_status_ready():
            time.sleep(pause)
            if chan.recv_ready():
                stdout += chan.recv(buff_size)

            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(buff_size)

        exit_status = chan.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            stdout += chan.recv(buff_size)

        while chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)

        # print "Result=>", exit_status, stdout, stderr
        return exit_status, stdout, stderr

def get_vc_thumbrpint():
    print("#######################################################")
    print("Getting the vCenter server Thumbprint for -", args.vc_ip)
    print("#######################################################")
    if args.vc_ip:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        count = 1
        while True:
            print("Trying to establish connection, Try:", count)
            try:
                print('Making connection to ' + args.vc_ip + ', using root credentails ')
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
        command = 'openssl x509 -in /etc/vmware-vpx/ssl/rui.crt -fingerprint -sha1 -noout'
        status, stdout, stderr = issue_command(ssh.get_transport(), 1, command)

        words = stdout.split("=")
        print("VC Thumbprint is - ", words[1])
        return words[1]


if __name__ == "__main__":
    vc_thumbprint = get_vc_thumbrpint()
    reg_nsxv(vc_thumbprint)