$tenant = $args[0]
$getVMsList = @{
    Method = "GET"
    Uri = "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances" 
    Authentication = "Bearer"
    Token = $(gcloud auth print-access-token) | ConvertTo-SecureString -AsPlainText -Force
    ContentType = "application/json"
}
$vminstances = Invoke-RestMethod @getVMsList
$vminstances.instances | Select-Object -Property name,userId,status | ConvertTo-Csv | Out-File "./VMs_$tenant.csv"