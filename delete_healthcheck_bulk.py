#!/usr/bin/env python3
import sys
import requests
import os
import json
import csv
import operator

def main(argv):
    argv = sys.argv[1:]
    file = open(argv[0], 'r')
    tenant = file.readlines()
    server = "vm-healthcheck"
    number = len(tenant)
    deleted_tenants = []
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
   
    for x in tenant:
        x = x.strip()
        try:
            print(f'Deleting tenant {x} - {server}. . . ')
            delete_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + x + "/vminstances/" + server
            instance_remove = requests.delete(delete_url, headers=headers, timeout=1)
        except requests.exceptions.ReadTimeout: 
            pass

    while number > len(deleted_tenants):
        deleted_tenants = []
        for x in tenant:
            x = x.strip()
            check_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + x + "/vminstances/" + server
            current_status = requests.get(check_url, headers=headers).json()    
            if  "message" in current_status:
                print(f'Tenant {x} - {server} is: {current_status["message"]}')
                deleted_tenants.append(x)

    
    print(f'Deleted vm-healthchecks in tenants [{len(deleted_tenants)}]: {deleted_tenants}')
   

if __name__ == "__main__":
   main(sys.argv)
