import boto
import boto.s3
from boto.s3.key import Key

#Put your id and key here
KEY_ID = ''
ACCESS_KEY = ''

s3_connection = boto.connect_s3(KEY_ID,ACCESS_KEY)

#bucket name = tst008
bucket = s3_connection.create_bucket('tst008',location=boto.s3.connection.Location.DEFAULT)

k = Key(bucket)

import sys
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

ifile = raw_input("Enter the file name.... : ")
k.key = 'tst008' + ifile
k.set_contents_from_filename(ifile, cb=percent_cb, num_cb=10)
