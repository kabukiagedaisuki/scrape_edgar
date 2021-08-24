#!/bin/sh

for a in `cat a`
do
	#echo "$a"
	python -m kabu financial -t $a
	sleep 1
done
