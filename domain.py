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

    file = open('tenants.txt', 'r')
    tenants = file.readlines()

       
    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}

    print("Tenant,Domain,UserVMs,UserQTY")
    
    for tenant in tenants:
        try:
            url_project = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip()
            url_instances = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip() + "/vminstances"
            url_users = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip() + "/users"
            project = requests.get(url_project, headers=headers)
            instances = requests.get(url_instances, headers=headers)
            users = requests.get(url_users, headers=headers)
            number = len(instances.json()['instances'])
            user = len(users.json()['users'])
            var = project.json()["name"] + "," + project.json()["domain"] + "," + str(number) + ","  + str(user)
            print(f'{var}')
        except Exception:
            print(f'{tenant.strip() + ",Project Not Found"}')
            continue


if __name__ == "__main__":
   main(sys.argv)
