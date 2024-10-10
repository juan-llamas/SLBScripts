#!/usr/bin/env python3
import sys
import requests
import os
import json
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
import threading  # Para obtener el ID del thread

# Variables globales para conteo de éxitos y fracasos, y almacenamiento de detalles
success_count = 0
failure_count = 0
successful_commands = []
failed_commands = []

def leer_tenant_y_server(archivo):
    with open(archivo, 'r') as f:
        for linea in f:
            tenant, server = linea.strip().split(',')
            yield tenant, server

def ejecutar_comando(tenant, server):
    #global success_count, failure_count, successful_commands, failed_commands
    command = '''sudo sh /usr/local/bin/renew-domain-admin-krb-ticket.sh; sleep 60; sudo klist -k -t'''

    # Autenticación y preparación del contexto en PowerShell
    token = os.popen("gcloud auth print-access-token").read().strip()
    headers = {"Authorization": "Bearer " + token}
    url_project = f"https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/{tenant}"
    project = requests.get(url_project, headers=headers).json()

    # Obtener el ID del proceso y el thread para este comando
    process_id = os.getpid()
    thread_id = threading.get_ident()

    print(f"Subproceso (PID: {process_id}, Thread: {thread_id}) ejecutando comando para {tenant}, {server}")

    try:
        if project["platform"] == "Azure":
            pwsh_command = f"""
                az account set --subscription '{tenant}'; az vm run-command invoke -g '{tenant}' -n '{server}' --command-id RunShellScript --scripts '{command}'
            """
            #pwsh_command = f"""Write-Host {thread_id}"""
            result = subprocess.run(['powershell.exe', '-Command', pwsh_command], capture_output=True, text=True)

            # Parsear el resultado JSON
            try:
                #print(result)
                output = json.loads(result.stdout)
                message = output["value"][0]["message"]
                print(f'Mensaje del comando:\n{message}')
            except json.JSONDecodeError:
                print('Error al parsear el JSON de la salida.')
                print(f'Salida completa:\n{result.stdout}')

            if result.returncode == 0:
                return (True, tenant, server)
            else:
                raise Exception(result.stderr)
        else:
            url_script = f"https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/{tenant}/vminstances/{server}"
            command_var = requests.get(url_script, headers=headers).json()
            if command_var["isLinux"] is True:
                pwsh_command = f"""
                    gcloud compute ssh linuxadminuser@{server} --command='{command}' --project={tenant} --zone={command_var['zone']} --tunnel-through-iap --quiet
                """
                result = subprocess.run(['powershell.exe', '-Command', pwsh_command], capture_output=True, text=True)

                # Parsear el resultado JSON
                try:
                    output = json.loads(result.stdout)
                    message = output["value"][0]["message"]
                    print(f'Mensaje del comando:\n{message}')
                except json.JSONDecodeError:
                    print('Error al parsear el JSON de la salida.')
                    print(f'Salida completa:\n{result.stdout}')

                if result.returncode == 0:
                    return (True, tenant, server)
                else:
                    raise Exception(result.stderr)
    except Exception as e:
        print(f'Error ejecutando comando para {tenant},{server}: {e}')
        return (False, tenant, server)

def procesar_resultado(resultado):
    global success_count, failure_count, successful_commands, failed_commands
    exito, tenant, server = resultado
    if exito:
        success_count += 1
        successful_commands.append(f'{tenant},{server}')
        print(f'Comando exitoso para {tenant},{server}')
    else:
        failure_count += 1
        failed_commands.append(f'{tenant},{server}')
        print(f'Comando fallido para {tenant},{server}')

def main():
    archivo_kerberos = 'kerberos.txt'
    #archivo_kerberos = 'kerberos _Ainternal.txt'
    #archivo_kerberos = 'kerberos_Apoc.txt'
    #archivo_kerberos = 'kerberos_Google.txt'
    max_workers = 2  # Número máximo de subprocesos simultáneos

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(ejecutar_comando, tenant, server) for tenant, server in leer_tenant_y_server(archivo_kerberos)]

        for future in as_completed(futures):
            resultado = future.result()
            procesar_resultado(resultado)

    # Resumen final
    print(f'\nResumen de ejecución:')
    print(f'Comandos exitosos: {success_count}')
    for cmd in successful_commands:
        print(cmd)

    print(f'Comandos fallidos: {failure_count}')
    for cmd in failed_commands:
        print(cmd)

if __name__ == "__main__":
    main()
