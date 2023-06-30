#!/bin/bash

echo "----------Creating the lines needed for the SAUTH CVX actvity-----------"

for i in $@
do 
	echo 'httpRequest.requestUrl=~"/api/v1/projects/(.*)/users/'"$i"'/sauth" OR'
done

echo "--------Printing keys----------"

for i in $@
do 
	echo "key(SAuth,'$i"\'\)
done

