# This script is created by Ravi Nandula - https://github.com/ravinandula/vmware_products/vRNI

import subprocess
import argparse

parser = argparse.ArgumentParser("This script will deploy vRNI Proxy using OVFTOOL")

parser.add_argument("--vrni-proxy-name", help="Provide vRNI VM Name", required=True)
parser.add_argument("--ds-name", help="Provide Datastore Name in the LAB VC", required=True)
parser.add_argument("--proxy_password", help="Provide a new password to set as proxy admin/root user password",
                    required=True)
parser.add_argument("--platform-secret-key", help="Provide vRNI Platform Secret Key", required=True)
parser.add_argument("--network-name", help="Provide Network Name in the LAB VC", required=True)
parser.add_argument("--vrni-proxy-ip", help="Provide vRNI Static IP", required=True)
parser.add_argument("--rp_name", help="Provide the child resource Pool ", required=True)
parser.add_argument("--proxy-ova", help="Provide Platform OVA details", required=True)
parser.add_argument("--netmask", help="Provide Netmask details of the vRNI Network", required=True)
parser.add_argument("--dns-server-ip", help="Provide DNS Server IP", required=True)
parser.add_argument("--gateway-ip", help="Provide Gateway address for vRNI deployment", required=True)
parser.add_argument("--domain-name", help="Provide Domain Name", required=True)
parser.add_argument("--ntp-server", help="Provide NTP Server Details", required=True)
parser.add_argument("--vc-sso-password", help="Provide VC SSO Password", required=True)
parser.add_argument("--lab-vc-ip", help="Provide LAB VC IP", required=True)
parser.add_argument("--dc-name", help="Provide Datacener Name in the LAB VC", required=True)
parser.add_argument("--cluster-name", help="Provide Cluster name in the LAB VC", required=True)
parser.add_argument("--master-rp-name", help="Provide Master Resource Pool Name in the LAB VC", required=True)

args = parser.parse_args()



def deploy_vrni_proxy(vrni_proxy_name, ds_name, network_name, vrni_proxy_ip, platform_secret_key, vrni_proxy_subnet,
                      vrni_proxy_gateway, dns_server, domain_name, ntp_server, vrni_proxy_password, proxy_ova,
                      vc_sso_password, lab_vc_ip, dc_name, cluster_name, partent_rp_name, rp_name):
    print("Deploying vRNI Proxy")


    vrni_proxy_command =  "ovftool   -dm=thin --X:enableHiddenProperties --X:logLevel=verbose " \
                            "--X:disableHostnameResolve --acceptAllEulas --allowExtraConfig --noSSLVerify " \
                            "--name='{0}' --datastore='{1}' --prop:Proxy_Shared_Secret='{2}' " \
                            " --deploymentOption=medium --network='{3}'  --viCpuResource=0:0:0 " \
                            "--viMemoryResource=0:0:0 --powerOn --X:waitForIp --prop:Auto-Configure=True  " \
                            "--prop:IP_Address='{4}' --prop:Netmask='{5}'  " \
                            "--prop:Default_Gateway='{6}' --prop:DNS='{7}' " \
                            "--prop:Domain_Search='{8}' --prop:NTP='{9}'   " \
                            "--prop:SSH_User_Password='{10}' --prop:CLI_User_Password='{10}' " \
                            " {11}  vi://administrator@vsphere.local:'{12}'@{13}/{14}/host" \
                            "/{15}/Resources/{16}/{17}".format(vrni_proxy_name, ds_name, platform_secret_key, network_name,
                                                               vrni_proxy_ip, vrni_proxy_subnet, vrni_proxy_gateway, dns_server,
                                                               domain_name, ntp_server, vrni_proxy_password, proxy_ova, vc_sso_password,
                                                               lab_vc_ip, dc_name, cluster_name,partent_rp_name, rp_name)

    print("vRNI Proxy Command -", vrni_proxy_command)

    output = subprocess.check_output(vrni_proxy_command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
    print("Got Output")
    print(output)

    output_lines = output.split("\n")
    for line in output_lines:
        if "Received IP address:" in line:
            received_ip = line
            actual_ip = received_ip.split(":")
            print(actual_ip)
            print("Final IP Address =>", actual_ip[1])
            return actual_ip[1]


if __name__ == "__main__":
    deploy_vrni_proxy (args.vrni_proxy_name, args.ds_name, args.network_name, args.vrni_proxy_ip, args.platform_secret_key,
                      args.netmask, args.gateway_ip, args.dns_server_ip, args.domain_name, args.ntp_server,
                      args.proxy_password, args.proxy_ova, args.vc_sso_password, args.lab_vc_ip, args.dc_name,
                      args.cluster_name, args.master_rp_name, args.rp_name)