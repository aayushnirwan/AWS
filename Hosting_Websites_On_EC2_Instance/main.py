import boto.ec2
from time import sleep

access_key_id = ""
secret_access_key = ""

REGION = "us-east-1"
AMI_ID = "ami-4fffc834"
EC2_KEY_HANDLE = "" #Your key pair filename
INSTANCE_TYPE = "t2.micro"
SECGROUP_HANDLE = "default"

#Use this Script or run script.py
user_data_script = """#!/bin/bash
sudo yum install update
sudo yum install -y httpd
sudo /usr/sbin/apachectl start
sudo easy_install awscli
sudo echo "[default]\naws_access_key_id = KEY_ID\naws_secret_access_key = ACCESS_KEY" >> ~/.aws/credentials
sudo aws s3 cp s3://webdevelopingonaws ./files/ --recursive
"""

print "Connecting to EC2"

conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

print "Launching instance with AMI-ID = %s\n with keypair = %s\n instance type = %s\n security group = %s\n"%(AMI_ID, EC2_KEY_HANDLE, INSTANCE_TYPE, SECGROUP_HANDLE)

reservation = conn.run_instances(AMI_ID,key_name=EC2_KEY_HANDLE,instance_type=INSTANCE_TYPE,security_groups=[SECGROUP_HANDLE])

instance = reservation.instances[0]

conn.create_tags([instance.id], {"Name":"Web Developing in AWS"})

print "Waiting for instance to be up and running"

status = instance.update()

while status == 'pending':
	print "Present state of Instance : %s" % instance.state
	sleep(10)
	status = instance.update()

if status == 'running':
	print "\nInstance is now running and instance details are:"
	print "Instance Size:" + str(instance.instance_type)
	print "Instance State:" + str(instance.state)
	print "Instance Launch Time:" + str(instance.launch_time)
	print "Instance Public DNS:" + str(instance.public_dns_name)
	print "Instance Private DNS:" + str(instance.private_dns_name)
	print "Instance IP:" + str(instance.ip_address)
	print "Instance Private IP:" + str(instance.private_ip_address)










