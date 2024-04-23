import base64
custom_deployment_json = '''{
      "name": "shared-storage",
      "version": "6.0.28",
      "properties": {
        "privateIp": "172.23.8.4",
        "vmSysprepVersion": "8.5.52",
        "imageRef": "shared-storage-image-20231226-1",
        "backupHourUtc": 19,
        "frequentSnapshots": 2,
        "hourlySnapshots": 0,
        "minSizeGb": "8192",
        "maxSizeGb": "131072",
        "driveLetter": "E",
        "label": "Shared Storage",
        "path": "/shared/data",
        "machineType": "Standard_D32s_v3",
        "diskType": "Premium_LRS"
      },
      "package": "shared-storage",
      "updateMode": "replace",
      "usePuppet": false,
      "updateStatusUsingPatch": true
    }'''
encodedBytes = base64.b64encode(custom_deployment_json.encode("utf-8"))
base64_encoded_custom_deployment = str(encodedBytes, "utf-8")
print(base64_encoded_custom_deployment)
