#! /bin/bash

#for i in $(cut -f 1  $1) ; do echo  "$i": \"false\", ; done
for i in $(grep -v "Contract not found" $1 | cut -f 1); do echo  \"name:$i\": \"false\", ; done
echo ""
echo "total Tenants: $(grep -v "Contract not found" $1|wc -l )"

for i in $(grep -v "Contract not found" $1| cut -f 1) ; do echo -n $i, ; done
