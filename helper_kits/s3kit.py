
import boto3
from app import app


class s3Kit(object):

    @staticmethod
    def upload_s3(file, key_name, content_type, bucket_name=app.config['S3_BUCKET_NAME'],
                  callback=None, md5=None, reduced_redundancy=False, acl="public-read"):

        try:
            # create connection
            # Create an S3 client
            s3 = boto3.client(
                's3',
                aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
            )
            s3.put_object(Bucket=bucket_name, Key=key_name,  Body=file)

            # s3.upload_file(file,
            #                   bucket_name,
            #                   key_name,
            #                   ExtraArgs={
            #                       "ACL": acl,
            #                       "ContentType": content_type
            #                     }
            #                   )
            return True
        except Exception as e:
            app.logger.error("Error upload: " + str(e))
            return False

    @staticmethod
    def download_s3():

        s3 = boto3.resource('s3')