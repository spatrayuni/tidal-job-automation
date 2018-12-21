#!/usr/bin/env bash

#Read from S3job properties and check if there was a release (check file timestamp for file within 24 hours)
file=`aws s3 cp s3://sms-automation-1/job_config.txt job1.txt`
value=`cat job1.txt` 

while IFS=, read -r nodes s3_path version; 
do
 number_of_nodes=$nodes	
 jar_location=$s3_path
 ifversion=$version
 

 #add latest EMR launch steps here
  
done <job1.txt

