$server = "vm-healthcheck"
$tenant = $args[0]


$currentStatus = @{
    Method = "GET"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server"
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}

$stopVM = @{
    Method = "POST"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/stop"
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}

$startVM = @{
    Method = "POST"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/start"
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}

$disk = @{
    Method = "GET"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/disks"
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}

$vmStatus = Invoke-RestMethod @currentStatus

if ( $vmStatus.status -ne "TERMINATED" )
{
Write-Host "---VM is not TERMINATED---"
Write-Host "Preparing for stopping VM..."
Invoke-RestMethod @stopVM

while ( $vmStatus.status -ne "TERMINATED" )
{
    Write-Host "Awating for VM server $server to be Shutdown in tenant: $tenant"
    Start-Sleep -Seconds 30
    $vmStatus = Invoke-RestMethod @currentStatus
}

Start-Sleep -Seconds 10
Write-Host "Waiting to Start VM..."
Invoke-RestMethod @startVM

while ( $vmStatus.status -ne "RUNNING" )
{
    Write-Host "Awating for VM server $server to be PowerOn in tenant: $tenant"
    Start-Sleep -Seconds 30
    $vmStatus = Invoke-RestMethod @currentStatus
}
}
elseif ( $vmStatus.status -eq "TERMINATED" )
{
Invoke-RestMethod @startVM

while ( $vmStatus.status -ne "RUNNING" )
{
    Write-Host "Awating for VM server $server to be PowerOn in tenant: $tenant"
    Start-Sleep -Seconds 30
    $vmStatus = Invoke-RestMethod @currentStatus
}
}

Start-Sleep -Seconds 30
Write-Host "$server rebooted. E drive mounted:"

$Currentdisks = Invoke-RestMethod @disk | ConvertTo-Json
Write-Host $Currentdisks 



