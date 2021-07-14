#!/bin/bash

#IPv4 C-Class(/24) Ping Sweeper.
#Syntax: ./ipsweep.sh XXX{1-3}.XXX{1-3}.XXX{1-3} (default to 192.168.1)
#Example: ./ipsweep.sh 192.168.0


if [ "$1" == "" ]; then
i='192.168.1'
else
if [ `echo $1 | grep -E '^(([0-9]{1,3})\.){2}[0-9]{1,3}$' | grep -vE '25[6-9]|2[6-9][0-9]|[3-9][0-9][0-9]'` ]; then
i=$1
else
echo "<Syntax>: $0 XXX{1-3}.XXX{1-3}.XXX{1-3} (default to 192.168.1)"
echo "<Example>: ./ipsweep.sh 192.168.0"
exit 1
fi
fi
for ip in `seq 1 254`; do
ping -4 -c 1 $i.$ip | grep "64 bytes" | head -1 | cut -d " " -f 4 | tr -d ":" &
done