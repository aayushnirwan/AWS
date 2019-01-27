import boto
import sys, os
from boto.s3.key import Key

LOCAL_PATH = ' '

#Put your id and key here
KEY_ID = ''
ACCESS_KEY = ''

s3_connection = boto.connect_s3(KEY_ID,ACCESS_KEY)

#Bucket name = tst008
bucket = s3_connection.get_bucket('tst008')

bucket_list = bucket.list()
for p in bucket_list:
  keystring = str(p.key)
  if not os.path.exists(LOCAL_PATH+keystring):
    p.get_contents_to_filename(LOCAL_PATH+keystring)

