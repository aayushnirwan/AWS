import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance
conn=boto.ec2.connect_to_region('us-east-2')
instance = conn.get_all_instances(['i-0ae3a6792468c19c5'])[0].instances[0]
ssh_client = sshclient_from_instance(instance,'newkeypair.pem',user_name='ec2-user')
print ssh_client.run('sudo yum install -y httpd')
