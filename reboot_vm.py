#!/usr/bin/env python3
import sys
import requests
from subprocess import PIPE, Popen
import time
import json

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


def main(argv):  
    argv = sys.argv[1:]

    if (len(argv)-1) < 1:
        tenant = argv[0]
        server = 'vm-healthcheck'
    else:
        tenant = argv[0]
        server = argv[1]

    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}
    url_status = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + server
    url_stop = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + server + "/stop"
    url_start = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + server + "/start"
    url_disks = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + server + "/disks"

    current_status = requests.get(url_status, headers=headers)

    if current_status.json()['status'] == 'TERMINATED' or current_status.json()['status'] == 'CLOUD VM STATUS: PowerState/deallocated':
        print (f'VM {server} is already {current_status.json()["status"]} state, proceeding to bring up...')
        requests.post(url_start, headers=headers)
        while current_status.json()['status'] != 'RUNNING':
            if current_status.json()['name'] == "ad-server" or current_status.json()['name'] == "admirror-server":
                current_status = requests.get(url_status, headers=headers)
                print (f'{current_status.json()["status"]}')
            else:
                current_status = requests.get(url_status, headers=headers)
                print (f'{current_status.json()["operationProgress"]} %')
            time.sleep(15)

    elif current_status.json()['status'] != 'TERMINATED' or current_status.json()['status'] != 'CLOUD VM STATUS: PowerState/deallocated':
        print (f'VM {server} is in {current_status.json()["status"]} state, proceeding to bring down...')
        requests.post(url_stop, headers=headers)
        time.sleep(10)
        current_status = requests.get(url_status, headers=headers)
        print (f'Waiting to Start VM {server}')
        time.sleep(10)
        requests.post(url_start, headers=headers)
        while current_status.json()['status'] != 'RUNNING':
            if current_status.json()['name'] == "ad-server" or current_status.json()['name'] == "admirror-server":
                current_status = requests.get(url_status, headers=headers)
                print (f'{current_status.json()["status"]}')
            else:
                current_status = requests.get(url_status, headers=headers)
                print (f'{current_status.json()["operationProgress"]} %')
            time.sleep(15)
        print (f'VM {server} ready...')
       
    print (f'VM {server} is already {current_status.json()["status"]} state, checking disks...')
    disks_status = requests.get(url_disks, headers=headers)
 
    print (f'{server} rebooted. Drives mounted:\n {json.dumps(disks_status.json()["disks"], indent=2)}')

if __name__ == "__main__":
   main(sys.argv)
