#!/usr/bin/env python3
import sys
import requests
import os
import time
import json
import re
import requests


def main(argv):  
    argv = sys.argv[1:]
    tenants = []
    if (len(argv)-1) < 1:
        file = open(argv[0], 'r')
        tenants = file.readlines()
        server = 'vm-healthcheck'
    else:
        tenants.append(argv[0])
        server = argv[1]
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    sysprep = r"vm-sysprep\\(.*)\\.*startup.ps1"
    print(f'Tenant,VM,Sysprep Version')
    for tenant in tenants:
        tenant = tenant.strip()
        url_log = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/"+ tenant +"/vminstances/" + server + "/log?alt=json" 
        log = requests.get(url_log, headers=headers).json()
        if  "message" in log:
            print(f'{tenant},{server},{log["message"]}')
        elif log['content'] != "":
            x = re.findall(sysprep, log['content'])
            print(f'{tenant},{server},{" ".join(x)}')
        else:
            print(f'{tenant},{server},Not log found')
    
if __name__ == "__main__":
   main(sys.argv)
