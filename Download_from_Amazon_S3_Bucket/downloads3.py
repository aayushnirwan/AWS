import boto
import sys, os
from boto.s3.key import Key

LOCAL_PATH = ' '
KEY_ID = 'AKIAJ73OFBSSBSFIJRWQ'
ACCESS_KEY = 'CgtsMkP6r85mXrwUVIEMR7wSZkgJtt0R9nIX0Vtr'

s3_connection = boto.connect_s3(KEY_ID,ACCESS_KEY)

bucket = s3_connection.get_bucket('tst008')

bucket_list = bucket.list()
for p in bucket_list:
  keystring = str(p.key)
  if not os.path.exists(LOCAL_PATH+keystring):
    p.get_contents_to_filename(LOCAL_PATH+keystring)

