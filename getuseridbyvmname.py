#!/usr/bin/env python3
import sys
import requests
import os
import json
import csv
import operator

def main(argv):
    tenant = sys.argv[1]
    vmname = sys.argv[2]
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    nextpagetoken = ""
    validation = 0
    #getusers_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/users?nextPageToken=" + nextpagetoken
    print(f'searching for UserID owner of  {vmname} on Tenant {tenant}. . .  ')
    while validation == 0: 
        try:
            getusers_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/users?nextPageToken=" + nextpagetoken
            getuser = requests.get(getusers_url, headers=headers,).json()
        except requests.exceptions.ReadTimeout: 
            pass
       
        for i in getuser['users']:
            if 'vmInstanceName' in i and i['vmInstanceName'] == vmname:
                print("===== Found UserID =====")
                print(i['vmInstanceName'])
                print(i['email'])
                validation=1
        nextpagetoken = getuser['nextPageToken']
        #print(nextpagetoken)

if __name__ == "__main__":
   main(sys.argv)
