
EMR Job automation
===================

This document outlines steps to automate parameterizing tidal job configuration. Here is the flow,

Jenkins --- > write job paramters like number of nodes, location of JAR file, version number to S3 

               - query S3 path for the jar file and store it in a environment variable JAR_filepath
               - Read git branch name for code repository and store it in a environment variable version_number
               - using the read_job_config.py query job configuration from DynamoDB table. JAR_filepath, version_number  will be passed as input parameter to the python script
               - write number_of_nodes, JAR_filepath, version_number into a txt file in S3


pre-requisites:
---------------

1. Update the read_job_config.py with S3 bucket and DynamoDB table name
2. configure EMRJob-mappings.json with DynamoDB table schema
3. Update DDB.py with DynamoDB table name you want to create and schema based on definitions in EMRJob-mappings.json
4. Update version.txt with required version values

Steps:
======

Set up a DynamoDB table that will store EMR cluster configuration
-----------------------------------------------------------------

1. Configure the EMRjob_mappings.json with job details like job name, number of nodes, scale, Ingest_Data_Size and any other parameters that you will require
2. In your terminal, configure AWS credentials for the AWS account in the required region and execute commant python DDB.py, this will create a DynamoDB table using the schema in EMRjob_mappings.json


Jenkins job configuration changes
----------------------------------

Update Jenkins job to add steps to set environment variable and execute python script to write to S3 bucket. Edit the Jenkins job configuration and add below steps,

1. Add command  git branch in the jenkins job step to read the branch name 

    $version = git branch

2. Add a command to read the s3 path into a environment variable
   
     $jar_filepath = s3://s3-bucket-name/key-name

3. Add a command to extract and assign versions to a variable
      #!/usr/bin/env bash
       value=`cat version.txt` 

       while IFS=, read -r old_version current_version new_version; 
      do
  
 
		  oldversion=${old_version//old_version=/}
		  currentversion=${current_version//current_version=/}
		  newversion=${new_version//new_version=/}
		  echo $oldversion
		  echo $currentversion
		  echo $newversion

		  if newversion not null,

		     calling tidal api to create historical/new job
		     <command for job creation along with parameters>
		  else
		  
		     exit   
       done <version.txt 

       To add:

         1. validate if new version is not null, if not null invoke tidal job creation

       tidal job creation:
       
          1. Identify if there is a API to automate tidal jobs
          2. can jenkins invoke the api ? if yes jenkins will need access to tidal
          3. define api parameters 
         


4. Add a step in Jenkins job called execute shell and configure it to execute the python script

     python read_job_config.py $currentversion $jar_filepath

5. save the jenkins and execute the job to test the changes. Validate the environment variables are set and that a file is created in S3 bucket with job property.


Update the EMR launch script to query the job properties from S3 Bucket
------------------------------------------------------------------------
1. In the EMR launch script, add the code to query config from S3 bucket and update the parameters for cluster provisioining code as needed refer (emr_launch.sh), below is the code


				#!/usr/bin/env bash

				#Read from S3job properties and check if there was a release (check file timestamp for file within 24 hours)
				file=`aws s3 cp s3://sms-automation-1/job_config.txt job1.txt`
				value=`cat job.txt` 

				while IFS=, read -r nodes s3_path version; 
				do
				 echo $nodes
				 echo $s3_path
				 echo $version 
				  
				done <job.txt

2. Test the EMR launch script from tidal portal and verify that job properties are read dynamically

