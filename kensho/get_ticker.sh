#!/bin/sh

curl -sk 'https://www.sec.gov/include/ticker.txt' | awk '{print $2,$1}' > ticker.txt

for cid in `awk '{print $1}' ticker.txt | sort -V | uniq -c | grep -v ' 1 ' | awk '{print $2}'`
do
    echo $cid
done
