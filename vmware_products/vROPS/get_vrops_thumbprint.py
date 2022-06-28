import subprocess, time
import json
import argparse

parser = argparse.ArgumentParser("This script will get the vROPS Thumbprint")

parser.add_argument("--vrops-ip", help="Provide vROPS IP Address", required=True)


args = parser.parse_args()

def get_vrops_thumbprint():
    print("Getting thumbprint of the vROPS Appliance ")

    retry_count=30
    while True:
        # Before running the thumbprint API check for the vROPS services status
        status_command='curl -s -o /dev/null -w "%{http_code}"  --request GET --header "Accept: application/json" ' \
                   '--include --insecure --silent https://'+args.vrops_ip.strip()+'/casa/slice/thumbprint'
        status_output = subprocess.check_output(status_command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')
        if status_output == str(200):
            print("VROPS Services are UP and we can get the Thumbprint")

            command='curl --request GET --header "Accept: application/json" --include --insecure ' \
               '--silent https://'+args.vrops_ip.strip()+'/casa/slice/thumbprint'

            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode('utf-8')

            output_lines = output.split("\n")
            for line in output_lines:
                print("########################################################")
                print(line)
                if '{"address":' in line:
                    d= json.loads(line)
                    print("Thumprint of the VROPS is - ", d["thumbprint"])
        elif status_output == str(503):
            if retry_count > 0:
                print("VROPS Services are not UP, Sleeping for 30 sec ")
                time.sleep(30)
            else:
                print("Reached the maximum retry count for Check the vROPS Service")
                raise Exception("Reached the maximum retry count for Check the vROPS Service")
        else:
            print("Could not get the 200 or 503 response code")
            raise Exception(status_output)

if __name__ == "__main__":
    get_vrops_thumbprint()