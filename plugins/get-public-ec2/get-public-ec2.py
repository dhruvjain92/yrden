import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class get_public_ec2(IPlugin):
    def execute(self):
        client = boto3.client("ec2")
        instance_dict = client.describe_instances().get("Reservations")
        instance_data = []
        for reservation in instance_dict:
            for instance in reservation["Instances"]:
                if "PublicIpAddress" in instance:
                    if self.output_format == "json":
                        instance_data.append(
                            {
                                "Instance_Id": instance["InstanceId"],
                                "Public_IP_Address": instance["PublicIpAddress"],
                            }
                        )
                    elif self.output_format == "table":
                        instance_data.append(
                            [instance["InstanceId"], instance["PublicIpAddress"]]
                        )
        if self.output_format == "json":
            speak(json.dumps(instance_data, indent=2, sort_keys=True))
        elif self.output_format == "file":
            self.write_to_file(instance_data)
            speak("File with output: " + self.output_file, "info")
        else:
            output_table = PrettyTable()
            output_table.field_names = ["Instance ID", "Public IP Address"]
            output_table.add_rows(instance_data)
            speak(output_table)

    def description(self):
        return """This plugin returns the public EC2 instances and their associated Public IP
        Created by: Dhruv Jain"""
