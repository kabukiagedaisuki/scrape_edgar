#!/bin/sh

safile=$1

#for i in `seq 1 30`
#do
#	for t in `cut -d' ' -f1 $safile | sort -u`
#	do
#		egrep "^$t " $safile | sed -n "${i}p" | egrep ' beat .* beat ' | awk '{print $1}'
#	done > last.$i
#
#	# if 0 byte filesize
#	if [ ! -s last.$i ]; then
#		rm last.$i 2>/dev/null
#	fi
#done

max=`ls -1tr last.* | tail -1 | cut -d'.' -f2`
comm -12 last.1 last.2 > tmp
for i in `seq 3 $max`
do
	comm -12 tmp last.$i > tmp-last.$i
	cp -p tmp-last.$i tmp
done
