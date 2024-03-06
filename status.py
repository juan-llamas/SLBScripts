#!/usr/bin/env python3
import sys
import requests
import os
import time
import json
import argparse

# Constants
SLEEP_INTERVAL = 10
BASE_URL = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/"

def banner(message, border='-'):
    line = border * len(message)
    print(line)
    print(message)
    print(line)

def get_access_token():
    try:
        return os.popen("gcloud auth print-access-token").read().strip()
    except Exception as e:
        print(f"Error retrieving access token: {e}")
        sys.exit(1)

def get_vm_status(tenant, server, headers):
    url_status = f"{BASE_URL}{tenant}/vminstances/{server}"

    try:
        return requests.get(url_status, headers=headers).json()
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return None

def print_vm_status(status):
    if "message" in status:
        banner(f'Error: {status["message"]}')
    elif "operationProgress" in status:
        banner(f'VM name: {status["name"]}\nStatus: {status["status"]}\nProgress: {status["operationProgress"]}%\nCreated: {status["created"]}')
    elif "operation" in status:
        banner(f'VM name: {status["name"]}\nStatus: {status["status"]}\nOperation: {status["operation"]}\nCreated: {status["created"]}')
    else:
        banner(f'VM name: {status["name"]}\nStatus: {status["status"]}')

def main():
    parser = argparse.ArgumentParser(description='Check VM status.')
    parser.add_argument('tenant', help='Tenant name')
    parser.add_argument('server', nargs='?', default='vm-healthcheck', help='Server name (default: vm-healthcheck)')
    args = parser.parse_args()

    headers = {"Authorization": "Bearer " + get_access_token()}

    print("Press ctrl-c to stop\n")
    try:
        while True:
            current_status = get_vm_status(args.tenant, args.server, headers)
            if current_status:
                print_vm_status(current_status)
                time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        print('Status execution exit()')

if __name__ == "__main__":
    main()
