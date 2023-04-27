#!/usr/bin/env python3
import sys
import requests
from subprocess import PIPE, Popen
import time
import json
import re

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def banner(message, border='-'):
    line = border * (len(message)-15)
    print(line)
    print(message)
    print(line)

def main(argv):  
    argv = sys.argv[1:]
    deploys = []
    if (len(argv)-1) < 1:
        tenant = argv[0]
        server = 'vm-healthcheck'
    else:
        tenant = argv[0]
        server = argv[1]
    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}
    url_deployments = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/deployments"
    deployments = ["ad-server","admirror-server","license-server","shared-storage","seismic-storage"]
    current_status = requests.get(url_deployments, headers=headers)


    for vm in current_status.json()["deployments"]:
        if re.search("filesync", vm['name']) or vm['name'] in deployments:
            deploys.append(vm['name'])
 
    
    print(",".join(deploys))
    


      

if __name__ == "__main__":
   main(sys.argv)
