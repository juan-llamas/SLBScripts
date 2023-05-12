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
    deploys = []
    argv = sys.argv[1:]
    tenant = argv[0]
    if (len(argv)-1) < 1:
        raise Exception(
            f'Virtual machine not specified') 
        sys.exit(1)
    else:
        tenant = argv[0]
        server = argv[1]
    command_cert_repo = f'''sudo dnf update -y --disablerepo=* --enablerepo='*microsoft*' rhui-azure-rhel8-eus'''
    command_copy_in = f'''sudo azcopy cp 'https://apisquery.blob.core.windows.net/opsbridge/opsbridge/install.sh?sp=racwdyti&st=2023-05-12T17:44:05Z&se=2023-06-01T01:44:05Z&spr=https&sv=2022-11-02&sr=b&sig=2%2Fxl4xL7d4xS%2BRMulpMIYBwkjDTFjxFNu72mKxSDfHM%3D' /usr/ --recursive'''
    command_copy_OA = f'''sudo azcopy cp 'https://apisquery.blob.core.windows.net/opsbridge/opsbridge/OA_12.22_LINUX.zip?sp=racwdyti&st=2023-05-12T17:42:33Z&se=2023-06-01T01:42:33Z&spr=https&sv=2022-11-02&sr=b&sig=WCnXBZmQPgfjFeLTsFb4IJhyFWzfRYVbDd8QPLMiEHk%3D' /usr/ --recursive'''
    command_install = f'''sudo chmod +x /usr/install.sh; sudo sh /usr/install.sh; sudo /opt/OV/bin/ovc -status'''
    token = str(cmdline("gcloud auth print-access-token").decode( "utf-8" ).strip())
    headers = {"Authorization": "Bearer " + token}
    url_project = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant
    deployments = ["ad-server","admirror-server","license-server","shared-storage","seismic-storage"]
    project = requests.get(url_project, headers=headers)

    if project.json()["platform"] == "Azure":
        if server in deployments:
            url_script = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/" + tenant + "/vminstances/" + server
            command_var = requests.get(url_script, headers=headers)
            if command_var.json()["isLinux"] is True:
                print(f'{server}')
                border='-'
                line = border * (80)
                command = os.system(f'az account set --subscription {tenant}')
                command = os.system(f'''az vm run-command invoke -g {tenant} -n {server} --command-id RunShellScript --scripts "{command_cert_repo}" ''')
                print("C o p y i n g  p a c k a g e s . . .")
                command = os.system(f'''az vm run-command invoke -g {tenant} -n {server} --command-id RunShellScript --scripts "{command_copy_in}" ''')
                print(command)
                command = os.system(f'''az vm run-command invoke -g {tenant} -n {server} --command-id RunShellScript --scripts "{command_copy_OA}" ''')
                print(command)
                print("I n s t a l l i n g . . .")
                command = os.system(f'''az vm run-command invoke -g {tenant} -n {server} --command-id RunShellScript --scripts "{command_install}" ''')
                print(command)
                print(line)
  

if __name__ == "__main__":
   main(sys.argv)
