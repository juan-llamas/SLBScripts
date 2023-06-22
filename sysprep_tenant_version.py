#!/usr/bin/env python3
import sys
import requests
import os
import json
import csv

def main(argv):  

    file = open('tenants.txt', 'r')
    exit_file = "sysprep.csv"
    tenants = file.readlines()

       
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}

    headerList = ["Tenant", "Sysprep Version"]
    with open(exit_file, 'w', newline='') as file2:
            dw = csv.DictWriter(file2, delimiter=',',
                        fieldnames=headerList)
            dw.writeheader()

    print("Tenant,Sysprep Version")

    for tenant in tenants:
        try:
            url_project = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip()
            project = requests.get(url_project, headers=headers).json()
            var = project["name"] + "," + project["version"]
            with open(exit_file,'a+') as file2:
                file2.write(var + "\n")
            print(f'{var}')
        except Exception:
            error = f'{tenant.strip() + ",Project Not Found"}'
            with open(exit_file,'a+') as file2:
                file2.write(error + "\n")
            print(f'{error}')
            continue


if __name__ == "__main__":
   main(sys.argv)
