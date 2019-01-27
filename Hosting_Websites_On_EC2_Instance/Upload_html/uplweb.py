import boto
import boto.s3
from boto.s3.key import Key

KEY_ID = ''
ACCESS_KEY = ''

s3_connection = boto.connect_s3(KEY_ID,ACCESS_KEY)

bucket = s3_connection.create_bucket('webdevelopingonaws',location=boto.s3.connection.Location.DEFAULT)

k = Key(bucket)

import sys
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

ifile = "index.html"
k.key = ifile
k.set_contents_from_filename(ifile, cb=percent_cb, num_cb=10)
