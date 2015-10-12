#!/bin/bash
day=$(date +%d)
month=$(LC_ALL=en_US.utf8 date +%b)
year=$(date +%Y)
for service in $(cat /var/spool/cron/crontabs/root | grep '/var/www/python/.*/manage.py autocharge -o' | awk {'print $1'})
	do
		echo $service
	done


