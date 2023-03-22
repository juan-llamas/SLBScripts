#!/usr/bin/env python3
import sys
import requests
from subprocess import PIPE, Popen
import time
import msvcrt

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
    

    print('Press "q" key to exit\n')
    while True:
        if msvcrt.kbhit() and msvcrt.getwch()=='q':
            break
        current_status = requests.get(url_status, headers=headers)
        print (f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}\nProgress: {current_status.json()["operationProgress"]}%\n')
        time.sleep(10)
    print('Status execution exit()')    
if __name__ == "__main__":
   main(sys.argv)
