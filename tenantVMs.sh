#!/bin/bash

TENANT=$1
TOKEN=$(gcloud auth print-access-token)
echo "Creating VM Report for $TENANT Tenant"
echo "--------------------------------------"
#curl -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/p-str-18201559-10495679/vminstances" -H "accept: application/json" -H "authorization: Bearer ya29.A0AVA9y1v1KoLmQs4RSyxKN-7hhsiZ-uZDvDcbmuOpzUh_66ceEojABQzjWKc3ezVs4wPeyfaLvBJI3ONI8t1QalHBzt1qV70sfwXSWg7c-iYhAfaH7ILY8NhfETkqOl8DPO4zj4cF7zRhZe-44uHXRreU28O_pUgYUNnWUtBVEFTQVRBU0ZRRTY1ZHI4U29JbHRZYm1MSWVLSUJoUTE5S2psQQ0166" | jq .instances[].name |sed 's/"//g'
 curl -s -X GET "https://p-pfs-slb-1-1bgapjz.uc.r.appspot.com/api/v1/projects/$TENANT/vminstances" -H "accept: application/json" -H "authorization: Bearer $TOKEN" | jq .instances[].name |sed 's/"//g' | tee "$TENANT-VM-Report" 
 echo "-------------------------------------"
 echo "Total VM's:" $(wc -l $TENANT-VM-Report)