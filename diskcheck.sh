#!/bin/bash

server="vm-healthcheck"
tenant=$1
token=$(gcloud auth print-access-token)

    ./rebootVM.sh $tenant $server
    sleep 30
    disk=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/disks" -H "accept: application/json" -H "authorization: Bearer $token")
    echo "$server rebooted. E drive mounted:"
    echo $disk | jq . 
