#!/usr/bin/env python3
import sys
import requests
import os
import json
import csv

def banner(message, border='-'):
    line = border * (len(message)-15)
    print(line)
    print(message)
    print(line)

def main():  
    # Check if the file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Open the file and read each line
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line
    for line in lines:
        # Split the line by comma to separate tenant and server
        tenant, server = line.strip().split(',')

        token = os.popen("gcloud auth print-access-token").read().strip()
        headers = {"Authorization": "Bearer " + token}

        try:
            url_status = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant.strip() + "/vminstances/" + server.strip()
            print(f'Tenant: {tenant}, Server: {server}')
            current_status = requests.get(url_status, headers=headers).json()
            if "message" in current_status:
                banner(f'Error: {current_status["message"]}')            
            elif "operationProgress" in current_status:
                banner(f'VM name: {current_status["name"]}\nStatus: {current_status["status"]}\nProgress: {current_status["operationProgress"]}%')
            elif "operation" in current_status:
                banner(f'VM name: {current_status["name"]}\nStatus: {current_status["status"]}\nOperation: {current_status["operation"]}')
            else:
                banner(f'VM name: {current_status["name"]}\nStatus: {current_status["status"]}')
        except Exception:
            error = f'{tenant.strip()},Project Not Found'
            banner(f'{error}')

if __name__ == "__main__":
   main()
