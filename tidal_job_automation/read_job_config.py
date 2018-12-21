# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with
# the License. A copy of the License is located at
#     http://aws.amazon.com/apache2.0/
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import os
import json
import boto3
import decimal
import ast
import time
from boto3.dynamodb.conditions import Key
import requests

array = []
version_number = sys.args[1]
s3_jar_location = sys.args[2]
inptstr = "job.txt"

dynamodb_client = boto3.client('dynamodb')
dynamodb_client = boto3.client('dynamodb')
tablename = 'DynamoDB-table-name'

s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)

#query job properties from DynamoDB table 
response = table.query(
        KeyConditionExpression=Key('Job_Name').eq("Feature-Creator-1") \
                               & Key("Scale").eq("Linear")
    )
for item in response['Items']:
        objkeypair = ast.literal_eval(item['mappings'])
        nodes = objkeypair["Average_Num_Nodes"]
    
        #array = nodes, s3_location,jar_name, version_number
        with open(inptstr,'w') as newfile:
            newfile.write(str(nodes))
            newfile.write(',') 
            newfile.write(str(s3_jar_location))
            newfile.write(',') 
            newfile.write(str(version_number))
            newfile.write('\n') 

        s3.Bucket('s3-bucket-name').upload_file(inptstr,'job_config.txt')


