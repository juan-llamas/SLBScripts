#!/usr/bin/env python3
import sys
import requests
from subprocess import PIPE, Popen
import time
import json
import re
import os

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def main(argv):  
    deploys = []
    argv = sys.argv[1:]
    tenant = argv[0]
    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}
    url_deployments = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/deployments"
    deployments = ["ad-server","admirror-server","license-server","shared-storage","seismic-storage"]
    current_deploys = requests.get(url_deployments, headers=headers)

    for vm in current_deploys.json()["deployments"]:
        if re.match(r"^filesync-(.+)", vm['name']) or vm['name'] in deployments:
            deploys.append(vm['name'])
            url_script = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + vm['name']
            command_var = requests.get(url_script, headers=headers)
            if command_var.json()["isLinux"] is True:
                os.system(f'gcloud compute ssh linuxadminuser@{command_var.json()["name"]} --command="pwd" --project={tenant} --zone={command_var.json()["zone"]} --tunnel-through-iap --quiet')
 
    
    print(",".join(deploys))
    

if __name__ == "__main__":
   main(sys.argv)
