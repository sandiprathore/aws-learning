![amazon-web-services-logo](https://user-images.githubusercontent.com/93520937/182449474-8ae7c2ec-bfbb-453a-95a4-98784b95944d.png)

#### Table of contents

AWS S3 with python
Read aws cloudwach logs using python

##### Prerequisites

* To start automating Amazon S3 operations and making API calls to the Amazon S3 service, you must first configure your Python environment.
* Python 3
* Boto3

##### Introduction

The Boto3 library provides you with two ways to access APIs for managing AWS services

1. The client that allows you to access the low-level API data. For example, you can access API response data in JSON format.
2. The resource that allows you to use AWS services in a higher-level object-oriented way


##### initialize the Boto3 client to start working with Amazon S3 APIs:

```py
import boto3

AWS_REGION = "<region_name>"
AWS_ACCESS_KEY_ID = "<aws_access_key_id>"
AWS_SECRET_ACCESS_KEY = "<aws_secret_access_key>"

client = boto3.client("s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION)
print('Boto3 client initialized successfully')
```

Using boto3.resource method:

```py
import boto3

AWS_REGION = "<region_name>"
AWS_ACCESS_KEY_ID = "<aws_access_key_id>"
AWS_SECRET_ACCESS_KEY = "<aws_secret_access_key>"

resource = boto3.resource("s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION)

print('Boto3 resource initialized successfully')
```


##### Creating S3 Bucket

* Using Boto3 client

```py
import boto3

client = boto3.client('s3')
bucket_name = '<bucket_name>'
location = {'LocationConstraint': '<aws_region>'}

response = client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
print('Amazon S3 bucket has been created')

```


<!--creating a s3 bucket using Boto3 resource -->
* Using Boto3 resource

```py
import boto3

resource = boto3.resource('s3')
bucket_name = '<bucket_name>'
location = {'LocationConstraint': '<aws_region>'}

bucket = resource.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration=location)
print('Amazon S3 bucket has been created')
```

<!--List the s3 buckets using Boto3 client -->
##### List S3 Buckets 

* using Boto3 client

```py
import boto3

client = boto3.client('s3')
response = client.list_buckets()
print('Listing s3 buckets:')

for bucket in response['Buckets']:
    print(f'-- {bucket['Name']}')
```

<!--List the s3 buckets using Boto3 resource -->
* Using Boto3 resource

```py
import boto3

resource = boto3.resource('s3')
iterator = resource.buckets.all()
print('Listing Amazon S3 Buckets:')

for bucket in iterator:
    print(f'-- {bucket.name}')
```

 <!-- Delete s3 Bucket using Boto3 client-->
##### Delete s3 Bucket

* using Boto3 client

```py
import boto3

client = boto3.client('s3')
bucket_name = '<bucket_name>'
client.delete_bucket(Bucket=bucket_name)
print('Amazon S3 Bucket has been deleted')
```

<!-- Delete s3 Bucket using Boto3 resource-->

* using Boto3 resource

```py
import boto3

resource = boto3.resource('s3')
bucket_name = '<bucket_name>'
s3_bucket = resource.Bucket(bucket_name)
s3_bucket.delete()
print('Amazon S3 Bucket has been deleted')
```


##### Download a directory from s3 using python

```py
import os 
import boto3

def download_directory_froms3(bucket_name, remote_directory_path):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)

    for obj in bucket.objects.filter(Prefix = remote_directory_path):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key)

download_directory_froms3('<bucket_name>', 'remote_directory_path')
```

#### Read aws cloudwach logs using python

**IAM policy to only list and read access for specific resource from cloudwatch logs**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:GetLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": "*",
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "true"
                }
            }
        }
    ]
}
```
`

**Python script read aws cloudwach logs** 

```py

LOG_GROUP_NAME='<log_group_name >'

def get_boto3_client_for_cloudwatch():
    """
    Get the boto3 client for cloudwatch logs
    Returns
    -------
    client: boto3.client
    botocore client for cloudwatch logs'  
        botocore client for cloudwatch logs'  
    """
    import boto3
    client = boto3.client('logs')
    return client


def get_log_stream_name(log_group_name: str)-> str:
    """
    Fetch the latest log stream name from cloudwatch
    Parameters
    ----------
    log_group_name: str
        cloudwatch log group name

    client : boto3 client
        for cloudwatch logs from 'get_boto3_client_for_logs' function
    Returns
    -------
    log_stream_name: str 
        latest log stream name from the log group
    """
    client = get_boto3_client_for_cloudwatch()
    log_stream = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime', 
        descending=True,
        limit=1  
    )
    log_stream_name = log_stream['logStreams'][0]['logStreamName']
    return log_stream_name


def get_cloudwatch_logs(
    log_stream_name: str,
    log_group_name: str
    ):
    """
    Fetch the logs of the from the cloudwatch 
    Parameters
    ----------
    log_stream_name: str
        cloudwatch log stream name
    log_group_name: str
        cloudwatch log group name
    
    """
    client = get_boto3_client_for_cloudwatch()
    log_events = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        limit=10,
        startFromHead=True|False
    )

    # list of events
    list_of_events = log_events['events']
    for event in list_of_events:
        # print logs from events
        print(event.get('message'))

log_group_name = LOG_GROUP_NAME
log_stream_name = get_log_stream_name(log_group_name)
cloudwatch_logs = get_cloudwatch_logs(log_stream_name,log_group_name)
```