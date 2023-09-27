$file = "C:\TEMP\all_projects.csv"
$nextpagetoken = ""
$ismoreinfo = $true
Add-Content -Path $file -Value "VM_name,Hostname,Status,OperationTime,TenantID,UserName,zone,userid,Image,CertificateDate,EngagementTyp"
$bearer = $(gcloud auth print-access-token)
$ten = "p-str-18201559-15160877"
$projects = (curl.exe -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$ten" -H "accept: application/json" -H "authorization: Bearer $bearer")
#$projects = (curl.exe -s -X GET "https://p-pfs-slb-1-1bgapjz.appspot.com/api/v1/projects" -H "accept: application/json" -H "authorization: Bearer $bearer")
$projs = ( Write-Output $projects | ConvertFrom-Json).name
foreach ($tenant in $projs) {
    Write-Output $tenant
    $bearer = $(gcloud auth print-access-token)
    while ($ismoreinfo){
        $vminfo = (curl.exe -s -X GET "https://p-pfs-slb-1-1bgapjz.appspot.com/api/v1/projects/$($tenant)/vminstances?nextPageToken=$nextpagetoken" -H "accept: application/json" -H "authorization: Bearer $bearer")
        $hname = ( Write-Output $vminfo | ConvertFrom-Json).instances
        foreach($h in $hname) {
            $expirydate = "None"
            if ( $h.status -Like "RUNNING") {
                Write-Output $h.hostname
                try{
                    [Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
                    $url = "https://"+$h.hostname+":42968/rdweb/"
                    $req = [Net.HttpWebRequest]::Create($url)
                    $req.Timeout = 6000
                    $req.GetResponse().dispose()
                    $expirydate = $req.ServicePoint.Certificate.GetExpirationDateString()
                }
                finally{
                    Write-Output $url
                }
            }
            Add-Content -Path $file -Value ($h.name+','+$h.hostname+','+$h.status+','+$h.operationTime+','+$tenant+','+$h.userFullName+','+$h.zone+','+$h.userId+','+$h.image+','+$expirydate+','+$projects.engagementType)
        }
            if(( Write-Output $vminfo | ConvertFrom-Json).nextPageToken -ne ""){
                $nextpagetoken = ( Write-Output $vminfo | ConvertFrom-Json).nextPageToken
            }
            else{   
                $ismoreinfo = $false
            }
    } #EndWhile
}
