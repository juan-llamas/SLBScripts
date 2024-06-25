#!/bin/bash

gettenants () {
	#for i in $(cat master); do echo $i | cut -d: -f2  ; done
	tenants=$(cut -d: -f2 $1 | sed 's/"//g')
	echo $tenants	
}

compare () {
	
	#echo "$1 $2"
	TENANTS=$(gettenants $1)
	#echo $TENANTS
	for i in $TENANTS; do
		#echo "evaluating tenant $i in file $2";
		grep $i $2 2>&1 > /dev/null || (LIST="$LIST $i" && writer $i) ;
	done
	#echo "$LIST"
	#echo "$LIST" |wc -w

}

writer () {
	echo "    \"name:$1\": \"false\","


}




compare $1 $2
