import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class public_s3(IPlugin):
    def execute(self):
        s3 = boto3.resource("s3")
        if self.output_format != "file":
            speak("Checking for Public Buckets", "warning")
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
            if self.AWS.check_public_bucket(bucket_name):
                self.add_to_output(
                    bucket_name,
                    "AWS::S3",
                    "This bucket is public",
                    {},
                    {"public_bucket": "true"},
                )

    def description(self):
        return """This plugin finds the public S3 buckets
        Created by: Dhruv Jain"""
