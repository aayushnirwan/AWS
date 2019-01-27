import boto.ec2.autoscale
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.cloudwatch import MetricAlarm
from boto.ec2.autoscale import ScalingPolicy
import boto.ec2.cloudwatch

access_key_id = ""
secret_access_key = ""

REGION = "us-east-2"
AMI_ID = "ami-0cf31d971a3ca20d6"
EC2_KEY_HANDLE = "newkeypair"
INSTANCE_TYPE = "t2.micro"
SECGROUP_HANDLE = "launch-wizard-1"

print "Connecting to AutoScaling Service"

conn = boto.ec2.autoscale.connect_to_region(REGION, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

print "Creating Launch Configuration"

lc = LaunchConfiguration(name='My-Launch-config-16', image_id=AMI_ID, key_name=EC2_KEY_HANDLE,instance_type=INSTANCE_TYPE,security_groups=[SECGROUP_HANDLE])

conn.create_launch_configuration(lc)

print "Creating AutoScaling Group"

ag = AutoScalingGroup(group_name='My-Group16', availability_zones=['us-east-2c'], launch_config=lc, min_size=1, max_size=2, connection=conn)

conn.create_auto_scaling_group(ag)

print "Creating Auto-scaling policies"

scale_up_policy = ScalingPolicy(name='scale_up', adjustment_type='ChangeInCapacity', as_name='My-Group16', scaling_adjustment=1,cooldown=180)

scale_down_policy = ScalingPolicy(name='scale_down', adjustment_type='ChangeInCapacity', as_name='My-Group16', scaling_adjustment=-1,cooldown=180)

conn.create_scaling_policy(scale_up_policy)
conn.create_scaling_policy(scale_down_policy)

scale_up_policy = conn.get_all_policies(as_group='My-Group16', policy_names=['scale_up'])[0]

scale_down_policy = conn.get_all_policies(as_group='My-Group16', policy_names=['scale_down'])[0]

print "Connecting to CloudWatch"

cloudwatch = boto.ec2.cloudwatch.connect_to_region(REGION, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

alarm_dimensions = {"AutoScalingGroupName":'My-Group15'}

print "Creating scale-up alarm"

scale_up_alarm = MetricAlarm(name='scale_up_on_cpu', namespace='AWS/EC2', metric='CPUUtilization', statistic='Average', comparison='>', threshold='70', period='60', evaluation_periods=2, alarm_actions=[scale_up_policy.policy_arn], dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_up_alarm)

print "Creating scale-down alarm"

scale_down_alarm = MetricAlarm(name='scale_down_on_cpu', namespace='AWS/EC2', metric='CPUUtilization', statistic='Average', comparison='<', threshold='50', period='60', evaluation_periods=2, alarm_actions=[scale_down_policy.policy_arn], dimensions=alarm_dimensions)

cloudwatch.create_alarm(scale_down_alarm)

print "Done!"
