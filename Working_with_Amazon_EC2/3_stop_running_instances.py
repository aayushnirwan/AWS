import boto.ec2
from time import sleep

ACCESS_KEY = ""
SECRET_KEY = ""

REGION = "us-east-2"

print "Connecting to EC2"
conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
print "Connection Successful"

print "Getting all instances"
reservation = conn.get_all_instances()
print reservation

for i in range(len(reservation)):
	instance_rs = reservation[i].instances
	instance = instance_rs[0]
	instanceid = instance_rs[0].id
	print "Stopping instance with ID : " + str(instanceid)

	conn.stop_instances(instance_ids=[instanceid])

	status = instance.update()
	while not status == 'stopped':
		print "Present state of Instance : " + instance.state
		sleep(10)
		status = instance.update()

	print "Stopped Instance with ID : " + str(instanceid)
