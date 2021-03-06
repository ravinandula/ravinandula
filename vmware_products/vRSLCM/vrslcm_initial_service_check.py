import  argparse, time, sys
import requests
requests.packages.urllib3.disable_warnings()



parser = argparse.ArgumentParser("This script will fetch the vRSLCM status after the initial Deployment")


parser.add_argument("--vrslcm-ip", help="Provide the vRSLCM IP", required=True)

args = parser.parse_args()

#Checking the VRSLCM Initial service start-up status check
def check_vrslcm_status(vrslcm_ip):
    print("Checking the vRSLCM Initial Service Start-Up")
    status_url = 'https://'+vrslcm_ip.strip()+'/lcm/bootstrap/api/status'

    headers = {'Accept': 'application/json, text/plain, */*'}

    retry_count = 40
    while True:
        r = requests.get(status_url, verify=False, headers=headers)

        if r.status_code != 200:
            print("Unable to get the 200 Status sync_and_convert_raw_data reports API", r.status_code)
            sys.exit(-1)
        if r.json()["status"] == None:
           if retry_count > 0:
               print("##################################################")
               print("Current Status is NULL, Hence sleeping for 60secs")
               print(r.text)
               print("##################################################")
               time.sleep(60)
           else:
               print("Retry count reached max, Hence quiting")
               print("############################################################################################")
               raise Exception("Retry count reached max, Hence quiting VRSLCM Initial Service Start-Up status check")

        elif r.json()["status"] == "INPROGRESS":
           if retry_count > 0:
               print("########################################################")
               print("Current Status is INPROGRESS, Hence sleeping for 60secs")
               print(r.text)
               print("########################################################")
               time.sleep(60)
           else:
               print("Retry count reached max, Hence quiting")
               print("##########################################################################################")
               raise Exception("Retry count reached max, Hence quiting VRSLCM Initial Service Start-Up status check")

        elif r.json()["status"] == "SUCCESS":
            print("########################")
            print("VRSLCM is ready to USE")
            print(r.text)
            print("########################")
            break
# main function
if __name__ == "__main__":
    check_vrslcm_status(args.vrslcm_ip)
    
   