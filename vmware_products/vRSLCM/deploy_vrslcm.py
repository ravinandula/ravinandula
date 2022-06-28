import  subprocess, argparse


parser = argparse.ArgumentParser("This script will deploy the VRSLCM through OVFTOOL")


parser.add_argument("--vrslcm-name", help="Provide VRSLCM VM Name", required=True)
parser.add_argument("--ds-name", help="Provide the Datastore Name on which all the VMs should be deployed", required=True)
parser.add_argument("--vrslcm-fqdn", help="Provide the vRSLCM FQDN", required=True)
parser.add_argument("--vrslcm-ip", help="Provide an FREE IP which can be used for VRSLCM deployment", required=True)
parser.add_argument("--rp-name", help="Provide the resource pool details", required=True)
parser.add_argument("--ovf-url", help="Provide the OVF Details", required=True)
parser.add_argument("--root-password", help="Provide the root password for VRSLCM, which will set at the "
                                            "time of deployment", required=True)
parser.add_argument("--ntp-server", help="Provide the NTP Server Details", required=True)
parser.add_argument("--network-gateway", help="Provide the Network Gateway IP", required=True)
parser.add_argument("--domain-name", help="Provide the domain name which wil be set in the LCM appliance", required=True)
parser.add_argument("--domain-server-ip", help="Provide the DNS Server IP", required=True)
parser.add_argument("--netmask", help="Provide the Netmask Details", required=True)
parser.add_argument("--vc-sso-username", help="Provide the VC SSO username", required=True)
parser.add_argument("--vc-sso-password", help="Provide the VC SSO Password", required=True)
parser.add_argument("--lab-vc-ip", help="Provide the LAB VC IP", required=True)
parser.add_argument("--dc-name", help="Provide the DC Name", required=True)
parser.add_argument("--cluster-name", help="Provide the Cluster Name", required=True)
parser.add_argument("--master-rp", help="Provide the master Resource Pool name", required=True)

args = parser.parse_args()

#Deploy vRSLCM through ovftool
def deploy_vrslcm(vrslcm_name, ds_name, vrslcm_fqdn, vrslcm_ip, rp_name, ovf_url, root_password, ntp_server,
                  network_gateway, domain_name, domain_server_ip, netmask, vc_sso_username, vc_sso_password, lab_vc_ip, dc_name, cluster_name, master_rp):


    vrslcm_command ="ovftool  --name='{0}' --X:injectOvfEnv   --noSSLVerify   " \
                    "--X:waitForIp   --diskMode=thin  --powerOn  --acceptAllEulas  --X:logFile=/tmp/ovftool.log " \
                    "--allowExtraConfig  --datastore='{1}' --network='VM Network'  " \
                    "--prop:vami.hostname='{2}' --prop:varoot-password='{6}' " \
                    "--prop:va-ssh-enabled=True --prop:va-firstboot-enabled=True --prop:va-telemetry-enabled=True " \
                    "--prop:va-ntp-servers='{7}' " \
                    "--prop:vami.gateway.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{8}' " \
                    "--prop:vami.domain.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{9}' " \
                    "--prop:vami.searchpath.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{9}' " \
                    "--prop:vami.DNS.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{10}' " \
                    "--prop:vami.ip0.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{3}' " \
                    "--prop:vami.netmask0.VMware_vRealize_Suite_Life_Cycle_Manager_Appliance='{11}'  " \
                    "{4}   vi://{12}:'{13}'@{14}/{15}/host/" \
                    "{16}/Resources/{17}/{5}".\
                    format(vrslcm_name, ds_name, vrslcm_fqdn, vrslcm_ip, ovf_url, rp_name, root_password, ntp_server,
                           network_gateway, domain_name, domain_server_ip, netmask, vc_sso_username, vc_sso_password,
                           lab_vc_ip, dc_name, cluster_name, master_rp)

    print("vRSLCM Command -", vrslcm_command)

    output = subprocess.check_output(vrslcm_command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
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

# main function
if __name__ == "__main__":
    deploy_vrslcm(args.vrslcm_name, args.ds_name, args.vrslcm_fqdn, args.vrslcm_ip, args.rp_name, args.ovf_url,
                  args.root_password, args.ntp_server, args.network_gateway, args.domain_name, args.domain_server_ip,
                  args.netmask, args.vc_sso_username, args.vc_sso_password, args.lab_vc_ip, args.dc_name,
                  args.cluster_name, args.master_rp)