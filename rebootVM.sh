#!/bin/bash

server=$2
tenant=$1
token=$(gcloud auth print-access-token)
currentStatus=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server" -H "accept: application/json" -H "authorization: Bearer $token" | jq .status | sed 's/"//g') 


    if [ "$currentStatus" != "TERMINATED" ]; then
        echo "---VM is not TERMINATED---"
        echo "Preparing for stopping VM..."
        curl -s -X POST "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/stop" -H "accept: text/plain" -H "authorization: Bearer $token"
        verify=$currentStatus
        while [ "$verify" != "TERMINATED" ]
        do
            echo "Awating for VM server $server to be Shutdown in tenant: $tenant"
            sleep 30
            verify=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server" -H "accept: application/json" -H "authorization: Bearer $token" | jq .status | sed 's/"//g') 
        done
        sleep 10
        echo "Waiting to Start VM..."
        curl -s -X POST "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/start" -H "accept: text/plain" -H "authorization: Bearer $token"
        verify=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server" -H "accept: application/json" -H "authorization: Bearer $token" | jq .status | sed 's/"//g') 
        while [ "$verify" != "RUNNING" ]
        do
            echo "Awating for VM server $server to be PowerOn in tenant: $tenant"
            sleep 30
            verify=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server" -H "accept: application/json" -H "authorization: Bearer $token" | jq .status | sed 's/"//g') 
        done

    elif [ "$currentStatus" == "TERMINATED" ]; then
        curl -s -X POST "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server/start" -H "accept: text/plain" -H "authorization: Bearer $token"
        verify=$currentStatus
        while [ "$verify" != "RUNNING" ] 
        do
            echo "Awating for VM server $server to be PowerOn in tenant: $tenant"
            sleep 30
            verify=$(curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$tenant/vminstances/$server" -H "accept: application/json" -H "authorization: Bearer $token" | jq .status | sed 's/"//g') 
        done
    fi
