# This script is created by Ravi Nandula - https://github.com/ravinandula/ravinandula

import argparse
import sys, os, time
import requests, urllib3
import json
import subprocess


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()

is_windows = sys.platform.startswith('win')

parser = argparse.ArgumentParser("This script will generate NSX Support Bundle")

parser.add_argument("--nsxip", help="Provide the VC SSO username", required=True)
parser.add_argument("--nsxusername", help="Provide the VC SSO username", required=False, default="admin")
parser.add_argument("--nsxpassword", help="Provide VC SSO password", required=True)
parser.add_argument("--downloaddir", help="Provide Directory path to download the NSX Support Bundle", required=True)

args = parser.parse_args()

def getSupportBundle():
    print "#####################"
    print "Getting the NSX UUID"
    print "#####################"
    uuidurl = 'https://'+ args.nsxip +'/api/v1/cluster/nodes'
    print "Running API", uuidurl
    try:
        command = "curl -u '{0}:{1}' -k {2}".format(args.nsxusername, args.nsxpassword, uuidurl)
        print "Running command to get the UUID", command
        output = subprocess.check_output(command, shell=True)
        value = json.loads(output)
        nsxuuid = value["results"][1]["external_id"]
        print "UUID of the NSX is : ", nsxuuid
        print "#####################################"
        print "Triggering Get NSX Support bundle API"
        print "####################################"
        supportbundleurl = 'https://'+ args.nsxip +'/api/v1/administration/support-bundles?action=collect'
        print "Running API to get NSX Support bundle", supportbundleurl
        payload = {"nodes": nsxuuid}
        scommand = "curl -d '{0}' -H \"Content-Type: application/json\" -X POST {1}  --insecure  --user '{2}:{3}'  --output {4}".format(
        payload, supportbundleurl, args.nsxusername, args.nsxpassword, args.downloaddir)
        print "Running Curl command  to get the support bundle ", scommand
        output = subprocess.check_output(scommand, shell=True)
        print "Successfull Created NSX Support Bundle"
        print "NSX Support Bundle is available in this location :", args.downloaddir
    except Exception as e:
        print "Unable to get the NSX Support Bundle"
        print e.output
        raise Exception(e)


if __name__ == "__main__":
    exit_code = 0
    try:
        getSupportBundle()
    except Exception as e:
        print e
        exit_code = 1
    finally:
        sys.exit(exit_code)
