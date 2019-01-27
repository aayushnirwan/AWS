import boto3
import pprint

access_key = ""
secret_key = ""
region = "us-east-2"

cluster_name = "BotoCluster"
service_name = "service_hello_world"
task_name = "hello_world"

ecs_client = boto3.client(
    'ecs',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

ec2_client = boto3.client(
    'ec2',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

def launch_ecs():
    response = ecs_client.create_cluster(
        clusterName=cluster_name
    )

    pprint.pprint(response)
    print("\n<--->\n")

    response = ec2_client.run_instances(
        ImageId="ami-0cf31d971a3ca20d6",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro"
        #IamInstanceProfile={
        #    "Name": "ecsInstanceRole"
        #},
        #UserData="#!/bin/bash \n echo ECS_CLUSTER=" + cluster_name + " >> /etc/ecs/ecs.config"
    )

    pprint.pprint(response)
    print("\n<--->\n")

    # Create a task definition
    response = ecs_client.register_task_definition(
        containerDefinitions=[
        {
          "name": "wordpress",
          "links": [
            "mysql"
          ],
          "image": "wordpress",
          "essential": True,
          "portMappings": [
            {
              "containerPort": 80,
              "hostPort": 80
            }
          ],
          "memory": 300,
          "cpu": 10
        },
        {
          "environment": [
            {
              "name": "MYSQL_ROOT_PASSWORD",
              "value": "password"
            }
          ],
          "name": "mysql",
          "image": "mysql",
          "cpu": 10,
          "memory": 300,
          "essential": True
        }
        ],
        family="hello_world"
    )

    pprint.pprint(response)
    print("\n<--->\n")


    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_name,
        desiredCount=1,
        clientToken='request_identifier_string',
        deploymentConfiguration={
            'maximumPercent': 250,
            'minimumHealthyPercent': 50
        }
    )

    pprint.pprint(response)
    print("\n<--->\n")


# Shut everything down and delete task/service/instance/cluster
def terminate_ecs():
    try:
        # Set desired service count to 0 (obligatory to delete)
        response = ecs_client.update_service(
            cluster=cluster_name,
            service=service_name,
            desiredCount=0
        )
        # Delete service
        response = ecs_client.delete_service(
            cluster=cluster_name,
            service=service_name
        )
        pprint.pprint(response)
        print("\n<--->\n")
    except:
        print("Service not found/not active")

    # List all task definitions and revisions
    response = ecs_client.list_task_definitions(
        familyPrefix=task_name,
        status='ACTIVE'
    )
    #pprint.pprint(response)

    # De-Register all task definitions
    for task_definition in response["taskDefinitionArns"]:
        # De-register task definition(s)
        deregister_response = ecs_client.deregister_task_definition(
            taskDefinition=task_definition
        )
        pprint.pprint(deregister_response)
        print("\n<--->\n")

    # Terminate virtual machine(s)
    response = ecs_client.list_container_instances(
        cluster=cluster_name
    )
    if response["containerInstanceArns"]:
        container_instance_resp = ecs_client.describe_container_instances(
            cluster=cluster_name,
            containerInstances=response["containerInstanceArns"]
        )
        for ec2_instance in container_instance_resp["containerInstances"]:
            ec2_termination_resp = ec2_client.terminate_instances(
                DryRun=False,
                InstanceIds=[
                    ec2_instance["ec2InstanceId"],
                ]
            )

    # Finally delete the cluster
    response = ecs_client.delete_cluster(
        cluster=cluster_name
    )
    pprint.pprint(response)


launch_ecs()
terminate_ecs()
