#!/usr/bin/env bash

#Read from S3job properties and check if there was a release (check file timestamp for file within 24 hours)
#file=`aws s3 cp s3://sms-automation-1/job_config.txt job1.txt`
value=`cat version.txt` 

while IFS=, read -r old_version current_version new_version; 
do
  
 
  oldversion=${old_version//old_version=/}
  currentversion=${current_version//current_version=/}
  newversion=${new_version//new_version=/}
  echo $oldversion
  echo $currentversion
  echo $newversion
done <version.txt

