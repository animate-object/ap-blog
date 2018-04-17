import logging
from os import environ

from botocore.exceptions import ClientError
from chalice import NotFoundError

from chalicelib.singletons import S3

BUCKET_NAME = environ.get('BUCKET_NAME')


def get_post(post_name):
    try:
        response = S3.get_object(
                Bucket=BUCKET_NAME,
                Key=post_name)['Body'].read()
        return response.decode('utf-8')
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'NoSuchKey':
            raise NotFoundError('No posts for key {}'.format(post_name))
        raise

def list_posts():
    try:
        response = S3.list_objects(
            Bucket=BUCKET_NAME
        )
        
        return [obj['Key'] for obj in 
                sorted(response['Contents'],
                    key=lambda p: p['LastModified'],
                    reverse=True)]
    except KeyError as ke:
        logging.warn("There's no content in the bucket, oh no!")
        return []
