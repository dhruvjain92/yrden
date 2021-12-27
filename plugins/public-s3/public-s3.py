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
        buckets = []
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
            if self.AWS.check_public_bucket(bucket_name):
                if self.output_format == "file":
                    buckets.append(bucket_name + "\n")
                else:
                    buckets.append(bucket_name)
        if self.output_format == "file":
            self.write_to_file(buckets)
        elif self.output_format == "json":
            speak(json.dumps(buckets, indent=2, sort_keys=True))
        else:
            output_table = PrettyTable()
            output_table.field_names = ["Bucket Name"]
            output_table.add_rows(buckets)
            speak(output_table)

    def description(self):
        return """This plugin finds the public S3 buckets
        Created by: Dhruv Jain"""
