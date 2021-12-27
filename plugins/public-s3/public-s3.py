import json
from core.plugin.IPlugin import IPlugin
from core.assistant import ask, speak
import boto3
from prettytable import PrettyTable
import re
import botocore


class public_s3(IPlugin):
    def execute(self):
        s3 = boto3.resource("s3")
        if self.output_format != "file":
            speak("Checking for Public Buckets", "warning")
        buckets = ["logistics-uploads-stage \n", "grofers-consumer-lego \n"]
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
            if self.AWS.check_public_bucket(bucket_name):
                if self.output_format == "file":
                    buckets.append(bucket_name + "\n")
                else:
                    buckets.append(bucket_name)
        if self.output_format == "file":
            self.write_to_file(buckets)

    def description(self):
        return """This plugin finds the public S3 buckets
        Created by: Dhruv Jain"""
