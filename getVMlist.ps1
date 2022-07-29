$tenant = $args[0]
Clear-Host
$getVMsList = @{
    Method = "GET"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances" 
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}
$userstenant = Invoke-RestMethod @getVMsList
$userstenant.instances | Select-Object -Property name,userId,status  |Format-Table | Out-File "./VMs_$tenant.txt"
