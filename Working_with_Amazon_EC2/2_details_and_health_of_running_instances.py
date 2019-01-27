import boto.ec2
from time import sleep

access_key_id = ""
secret_access_key = ""

REGION = "us-east-2"

print "Connecting to EC2"
conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
print "Connection Successful"
print "Getting Information about all running instances...."

reservation = conn.get_all_instances()
status = conn.get_all_instance_status()

print reservation

for item in reservation:
	instances = item.instances
	i = 0
	for instance in instances:
		print "______\n"
		print "Instance Size : " + str(instance.instance_type)
		print "Instance State : " + str(instance.state)
		print "Instance Launch Time : " + str(instance.launch_time)
		print "Instance Public DNS : " + str(instance.public_dns_name)
		print "Instance Private DNS : " + str(instance.private_dns_name)
		print "Instance IP : " + str(instance.ip_address)
		print "Instance Private IP : " + str(instance.private_ip_address)
		print "System_status : " + status[i].system_status.status + " and " + "Instance_status : " + status[i].instance_status.status
		i+=1
