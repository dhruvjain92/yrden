import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class get_public_ec2(IPlugin):
    def execute(self):
        client = boto3.client("ec2")
        instance_dict = client.describe_instances().get("Reservations")
        for reservation in instance_dict:
            for instance in reservation["Instances"]:
                if "PublicIpAddress" in instance:
                    self.add_to_output(
                        instance["InstanceId"], "AWS::EC2", "Public EC2 Instance"
                    )

    def description(self):
        return """This plugin returns the public EC2 instances and their associated Public IP
        Created by: Dhruv Jain"""
