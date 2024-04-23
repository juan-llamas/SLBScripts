#!/usr/bin/env python3
import sys
import requests
import os
import json
import csv
import operator

def main(argv):  
    argv = sys.argv[1:]
    tenant = argv[0]
    file_out = "vm_" + tenant + ".csv"
    nextpagetoken = ""
    validation = 0
    headercsv = ['VM name', 'User ID', 'Status']
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    with open(file_out, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headercsv)
    f.close()
    print(','.join(headercsv))
    while validation == 0:
        instance_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances?nextPageToken=" + nextpagetoken
        instance_call = requests.get(instance_url, headers=headers).json()
        with open(file_out, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            for instance in instance_call["instances"]:
                vm_name = instance.get("name", "")
                user_id = instance.get("userId", "")  # Default value if 'userId' is missing
                status = instance.get("status", "")    # Default value if 'status' is missing
                line = [vm_name, user_id, status]
                print(",".join(line))
                writer.writerow(line)
        f.close()
        nextpagetoken = instance_call['nextPageToken']
        if not nextpagetoken:
            validation = 1

if __name__ == "__main__":
   main(sys.argv)
