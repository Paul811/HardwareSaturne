#!/bin/bash
value=$(<nomDiffuseur.txt)
sudo hciconfig hci0 name $value
sudo hciconfig hci0 reset
sleep 1
sudo hciconfig hci0 piscan
sleep 1
if [ "$1" ]
then
	sudo python ./script.py $1
else
	sudo python ./script.py AucunParfum
fi

