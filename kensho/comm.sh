#!/bin/sh

ticker=$1
earnings=$2

IFS='
'
for l in `sort $ticker`
do
	t=`echo $l | awk '{print $1}'`
	c=`echo $l | awk '{print $2}'`

    if [ `grep -c ^"$t " $earnings` -eq 0 ]; then
		echo "$t $c"
	fi
done
