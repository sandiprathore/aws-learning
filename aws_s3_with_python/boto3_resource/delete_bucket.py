import boto3

AWS_REGION = "<region_name>"
AWS_ACCESS_KEY_ID = "<aws_access_key_id>"
AWS_SECRET_ACCESS_KEY = "<aws_secret_access_key>"

resource = boto3.resource('s3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name=AWS_REGION)

bucket_name = "<bucket_name>"

s3_bucket = resource.Bucket(bucket_name)
s3_bucket.delete()

print("Amazon S3 Bucket has been deleted")