import subprocess
import argparse

parser = argparse.ArgumentParser("This script will deploy vRNI using OVFTOOL")

parser.add_argument("--vrni-platform-name", help="Provide vRNI VM Name", required=True)
parser.add_argument("--ds-name", help="Provide Datastore Name in the LAB VC", required=True)

parser.add_argument("--network-name", help="Provide Network Name in the LAB VC", required=True)
parser.add_argument("--vrni-platform-ip", help="Provide vRNI Static IP", required=True)
parser.add_argument("--rp_name", help="Provide the child resource Pool ", required=True)
parser.add_argument("--platform-ova", help="Provide Platform OVA details", required=True)
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



#Deploying vRNI using ovftool
def deploy_vrni_platform(vrni_platform_name, ds_name, network_name, vrni_platform_ip, rp_name, platform_ova, netmask,
                         dns_server_ip, gateway_ip, domain_name, ntp_server, vrni_password, vc_sso_password, lab_vc_ip,
                         dc_name, cluster_name, master_rp_name):
    print("Deploying vRNI 6.5 Platform")



    vrni_platform_command= "/home/worker/ovftool/ovftool -dm=thin --X:enableHiddenProperties --X:logLevel=verbose " \
                 "--X:disableHostnameResolve --acceptAllEulas --allowExtraConfig --noSSLVerify " \
                 "--name='{0}' --datastore='{1}' --deploymentOption='medium' --network='{2}' --viCpuResource=:0:" \
                 "  --viMemoryResource=:0: --overwrite --powerOffTarget --powerOn --X:waitForIp " \
                 "--prop:Auto-Configure=True --prop:IP_Address='{3}' --prop:Netmask={6} " \
                 "--prop:DNS={7} --prop:Default_Gateway={8} --prop:Domain_Search={9} " \
                 "--prop:NTP={10} --prop:SSH_User_Password='{11}' --prop:CLI_User_Password='{11}'" \
                 "  {4}  vi://administrator@vsphere.local:'{12}'@{13}/{14}/host/{15}/" \
                 "Resources/{16}/{5}".format(vrni_platform_name, ds_name, network_name,
                  vrni_platform_ip, platform_ova, rp_name, netmask, dns_server_ip, gateway_ip, domain_name, ntp_server,
                  vrni_password, vc_sso_password, lab_vc_ip, dc_name, cluster_name, master_rp_name)

    print("vRNI Platform Command -", vrni_platform_command)

    output = subprocess.check_output(vrni_platform_command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
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
    deploy_vrni_platform(args.vrni_platform_name, args.ds_name, args.network_name, args.vrni_platform_ip, args.rp_name,
                         args.platform_ova, args.netmask, args.dns_server_ip, args.gateway_ip, args.domain_name,
                         args.ntp_server, args.vrni_password, args.vc_sso_password, args.lab_vc_ip, args.dc_name,
                         args.cluster_name, args.master_rp_name)