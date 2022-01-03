import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class get_buckets_versioning(IPlugin):
    def execute(self):
        s3 = boto3.resource("s3")
        speak("Checking for Buckets for versioning status", "warning")
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
            versioning = "false"
            if self.AWS.check_s3_versioning(bucket_name):
                versioning = "true"
            self.add_to_output(
                bucket_name,
                "AWS::S3",
                "Bucket versioning is enabled for this bucket",
                {},
                {"versioning": versioning},
            )

    def description(self):
        return """This plugin finds the public S3 buckets
        Created by: Dhruv Jain"""
