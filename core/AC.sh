#!/bin/bash
day=$(date +%d)
month=$(LC_ALL=en_US.utf8 date +%b)
year=$(date +%Y)
log_file=/var/log/cron-log/
grep '$day/$month/$year' $log_file/$1 | wc -l