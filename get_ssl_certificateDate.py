#!/usr/bin/env python3
import sys
import os
import json
import csv
import operator
import OpenSSL
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime
import requests
import ssl


def get_certificate_expiry_date(url):
    # Extracting hostname and port from the URL
    parsed_url = requests.utils.urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443

    # Establishing a connection and retrieving the SSL certificate
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
            x509_cert = x509.load_der_x509_certificate(der_cert, default_backend())
            expiry_date = x509_cert.not_valid_after
            return expiry_date


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File recreated: {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except PermissionError:
        print(f"Permission error: Unable to delete {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main(argv):  
    argv = sys.argv[1:]
    tenant = argv[0]
    file_path_to_delete = "vm_" + tenant + ".csv"
    delete_file(file_path_to_delete)
    file_out = "vm_" + tenant + ".csv"
    nextpagetoken = ""
    validation = True
    notheaders = True
    headercsv = ['VM_name',	'Hostname', 'Status', 'OperationTime', 'TenantID', 'UserName', 'zone', 'userid', 'Image', 'EngagementTyp', 'ExpiryDate']
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    project_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant
    project_call = requests.get(project_url, headers=headers).json()
    while validation:
        instance_url = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances?nextPageToken=" + nextpagetoken
        instance_call = requests.get(instance_url, headers=headers).json()
        print(','.join(headercsv))
        with open(file_out, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            if notheaders is True:
                writer.writerow(headercsv)
                notheaders = False
            for instance in instance_call["instances"]:
                if not "userFullName" in instance or not "userId" in instance:
                    instance["userFullName"] = "null"
                    instance["userId"] = "null"
                if instance['status'] == "RUNNING":
                    url = f"https://{instance['hostname']}:42968/rdweb/"
                    expiry_date = get_certificate_expiry_date(url)
                    formatted_expiry_date = expiry_date.strftime("%d-%m-%Y")
                    instance['tenantID'] = tenant
                    instance['engagementType'] = project_call["engagementType"]
                    instance['expiryDate'] = formatted_expiry_date
                    line = operator.itemgetter("name", "hostname", "status", "operationTime", "tenantID", "userFullName", "zone", "userId", "image", "engagementType", "expiryDate")(instance)
                    print(",".join(line))
                    writer.writerow(line)
                else:
                    print(f"VM is PowerOff: {instance['name']}")
                    line = f"VM is PowerOff: {instance['name']}"
                    writer.writerow([line])
        f.close()
        nextpagetoken = instance_call['nextPageToken']
        if not nextpagetoken:
            validation = False

if __name__ == "__main__":
   main(sys.argv)
