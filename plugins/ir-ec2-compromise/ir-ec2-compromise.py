import json
from core.plugin.IPlugin import IPlugin
from core.assistant import run, speak
import boto3
from prettytable import PrettyTable
import re


class ir_ec2_compromise(IPlugin):

    # This group allows incoming requests from the server where this solution is hosted.
    aws_ec2_ir_sg_id = ""

    def execute(self):
        try:
            self.isolate_instance(self.instance_id)
            self.create_snapshots(self.instance_id)
            # self.ec2_forensics(self.instance_id)
        except Exception as e:
            speak(e, "error")

    def isolate_instance(self, instance_id):
        ec2 = boto3.resource("ec2")
        instance = ec2.Instance(instance_id)
        speak("Isolating Instance...", "warning")
        security_groups = [self.aws_ec2_ir_sg_id]
        instance.modify_attribute(Groups=security_groups)
        speak("Instance: " + self.instance_id + " has been isolated.", "info")
        instance.modify_attribute(DisableApiTermination={"Value": True})
        speak("Termination protection has been added to the instance.", "info")

    def create_snapshots(self, instance_id):
        ec2 = boto3.resource("ec2")
        instance = ec2.Instance(instance_id)
        speak("Creating snapshots")
        for device in instance.block_device_mappings:
            volume_id = device.get("Ebs").get("VolumeId")
            speak("Creating snapshot for : " + volume_id + "...", "warning")
            snapshot = ec2.create_snapshot(
                VolumeId=volume_id,
                Description="Snapshot created for instance: "
                + instance_id
                + " by  Yrden",
            )
            print(snapshot)
            speak(
                "Snapshot creation with ID: "
                + snapshot.snapshot_id
                + " has been started!",
                "info",
            )

    # def ec2_forensics(self, instance_id):
    #     sandbox_bucket = "security-test-yrden"
    #     commands = [
    #         "echo 'Files List:'",
    #         "ls /",
    #         "echo Linux Distribution",
    #         "uname -a > test",
    #         "",
    #     ]
    #     ssmclient = boto3.client("ssm")
    #     ssmclient.send_command(
    #         InstanceIds=[instance_id],
    #         DocumentName="AWS-RunShellScript",
    #         Parameters={
    #             "commands": commands,
    #             "executionTimeout": ["600"],  # Seconds all commands have to complete in
    #         },
    #         Comment="SSM Command Execution",
    #         OutputS3Region="us-west-2",
    #         OutputS3BucketName=sandbox_bucket,
    #         OutputS3KeyPrefix=instance_id,
    #     )

    #     ssmclient.send_command(
    #         DocumentName="AWS-RunShellScript",
    #         Parameters={"commands": self.memory_dump_commands(sandbox_bucket)},
    #         InstanceIds=[instance_id],
    #     )

    # def memory_dump_commands(self, sandbox_bucket):
    #     commands = [
    #         "sudo apt-get install git -y",
    #         "sudo apt-get install kernel-devel-$(uname -r) -y",
    #         "sudo apt-get install gcc -y",
    #         "cd /tmp/",
    #         "sudo git clone https://github.com/504ensicsLabs/LiME",
    #         "cd LiME/src",
    #         "sudo make",
    #         "sudo cp ./lime-$(uname -r).ko s3://{sandbox_bucket}",
    #         "sudo make clean",
    #     ]
    #     return commands

    # def basic_forensics(self, sandbox_bucket):
    #     commands = []
    #     return commands

    def description(self):
        return """
        This will isolate the impacted instance and create a snapshot.\n
        """

    def pre_execution(self):
        if self.aws_ec2_ir_sg_id == "":
            run(
                "The restricted Security Group is not updated in the code. This group allows us to run commands after isolation."
            )
        self.install_plugin_dependencies({"awscli"})
        self.instance_id = self.get_req_value("instanceId")
        return super().pre_execution()

    def post_execution(self):
        pass
