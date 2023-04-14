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

def banner(message, border='-'):
    line = border * (len(message)-15)
    print(line)
    print(message)
    print(line)

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
    print("Press ctrl-c to stop\n")
    loop_forever = True
    while loop_forever:
        try:
            current_status = requests.get(url_status, headers=headers)
            if  "message" in current_status.json():
                banner(f'Error: {current_status.json()["message"]}')
                time.sleep(10)
            elif current_status.json()["name"] == 'ad-server' or current_status.json()["name"] == 'admirror-server' or current_status.json()["name"] == 'shared-storage' or current_status.json()["name"] == 'seismic-storage' or current_status.json()["name"] == 'license-server':
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}')
                time.sleep(10)
            elif "operationProgress" in current_status.json():
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}\nProgress: {current_status.json()["operationProgress"]}%')
                time.sleep(10)
            else:
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}\nOperation: {current_status.json()["operation"]}')
                time.sleep(10)
        except KeyboardInterrupt:
            loop_forever = False
    print('Status execution exit()')    

if __name__ == "__main__":
   main(sys.argv)
