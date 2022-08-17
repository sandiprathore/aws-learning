import boto3

AWS_REGION = "<region_name>"
AWS_ACCESS_KEY_ID = "<aws_access_key_id>"
AWS_SECRET_ACCESS_KEY = "<aws_secret_access_key>"


client = boto3.client("s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION)
            
response = client.list_buckets()

print("Listing Amazon S3 Buckets:")

for bucket in response['Buckets']:
    print(f"-- {bucket['Name']}")