# SLBScripts
Scripts that will help regarding supporting SLB

`git clone https://github.com/eccervantes/SLBScripts.git`

`cd SLBScripts`

`chmod +x *.sh`


# Uso tenantVM.sh

`./tenantVM.sh <tenant>`

* this script will create a file with the name of the tenant´s VMS, make sure you specified the tenant as an argument, will provided also with the total numbers of VMS.

# Uso Cleandata.sh

`./cleandata.sh <FILE>`

# Use Reboot VM-healthcheck bash .sh

`./diskcheck.sh <tenant>`

# Uso del script Reboot ANY VM bash .sh

`./rebootVM.sh <tenant> <vm_name>`

# Uso del script Reboot VM-healthcheck powershell

`./rebootVM.ps1 <tenant>`

# Uso del script report.py (descargar file csv de querys y correr mismo path script)

`python3 report.py <file.csv>`

# Uso del script reboot_vm.py (sin VM name la default VM es vm-healthcheck)

`python3 reboot_vm.py <tenant> <optional vm name>`

# Uso del script status.py (sin VM name la default VM es vm-healthcheck)

`python3 status.py <tenant> <optional vm name>`

# TGX check

`sudo /license/licserver status 
shutdown -r now t
he log is in /license/debug.log ./lmutil lmstat -a`
