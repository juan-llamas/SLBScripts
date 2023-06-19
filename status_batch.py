#!/usr/bin/env python3
import sys
import requests
from subprocess import PIPE, Popen
import json
import csv

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


def main():  

    server = 'vm-healthcheck'
    file = open('tenants.txt', 'r')
    tenants = file.readlines()

       
    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}

    for tenant in tenants:
        try:
            url_status = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip() + "/vminstances/" + server
            print(f'{tenant}')
            current_status = requests.get(url_status, headers=headers)
            if  "message" in current_status.json():
                banner(f'Error: {current_status.json()["message"]}')            
            elif "operationProgress" in current_status.json():
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}\nProgress: {current_status.json()["operationProgress"]}%')
            elif "operation" in current_status.json():
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}\nOperation: {current_status.json()["operation"]}')
            else:
                banner(f'VM name: {current_status.json()["name"]}\nStatus: {current_status.json()["status"]}')
        except Exception:
            error = f'{tenant.strip() + ",Project Not Found"}'
            banner(f'{error}')
            continue


if __name__ == "__main__":
   main()
