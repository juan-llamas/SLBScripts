#!/usr/bin/env python3
import sys
import requests
import os
import json
import re

def main(argv):
    tenant = sys.argv[1]
    vmname_user = sys.argv[2]
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    nextpagetoken = ""
    validation = 0
    x = re.search('.com$', vmname_user)
    print(f'searching for UserID owner of  {vmname_user} on Tenant {tenant}. . .  ')
    if(x==None): 
        while validation == 0: 
                try:

                    getusers_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/users?nextPageToken=" + nextpagetoken
                    getuser = requests.get(getusers_url, headers=headers,).json()
                except requests.exceptions.ReadTimeout: 
                    pass 
                for i in getuser['users']:
                    if 'vmInstanceName' in i and i['vmInstanceName'] == vmname_user:
                        print("===== Found UserID =====")
                        print(i['vmInstanceName'])
                        print(i['email'])
                        validation=1
                nextpagetoken = getuser['nextPageToken']
    else:
        try:
            getvm_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/users/" + vmname_user
            getvm = requests.get(getvm_url, headers=headers,).json()
            print("===== Found VM =====")
            print(getvm['vmInstanceName'])
            print(getvm['email'])
        except Exception:
            error = f'{tenant.strip() + ", VM not found"}'
            print(f'{error}')


if __name__ == "__main__":
   main(sys.argv)
