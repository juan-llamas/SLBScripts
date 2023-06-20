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
    headercsv = ['VM name', 'User ID', 'Status']
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    instance_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances"
    instance_call = requests.get(instance_url, headers=headers).json()
    print(','.join(headercsv))
    with open(file_out, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headercsv)
        for instance in instance_call["instances"]:
            line = operator.itemgetter("name", "userId", "status")(instance)
            print(",".join(line))
            writer.writerow(line)
    f.close()

if __name__ == "__main__":
   main(sys.argv)
