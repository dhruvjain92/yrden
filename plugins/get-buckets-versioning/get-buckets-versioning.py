import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable


class get_buckets_versioning(IPlugin):
    def execute(self):
        s3 = boto3.resource("s3")
        if self.output_format != "file":
            speak("Checking for Buckets for versioning status", "warning")
        bucket_info = None
        if self.output_format == "json":
            bucket_info = {}
            bucket_info = {"enabled": [], "disabled": []}
        elif self.output_format == "file":
            bucket_info = []
            bucket_info.append("BucketName,VersioningStatus")
        else:
            bucket_info = []
        for bucket in s3.buckets.all():
            bucket_name = bucket.name
            if self.AWS.check_s3_versioning(bucket_name):
                self.add_to_output(bucket_info, bucket_name, "Enabled")
            else:
                self.add_to_output(bucket_info, bucket_name, "Disabled")
        if self.output_format == "file":
            self.write_to_file(bucket_info)
        elif self.output_format == "json":
            speak(json.dumps(bucket_info, indent=2, sort_keys=True))
        else:
            output_table = PrettyTable()
            output_table.field_names = ["Bucket Name", "Versioning Status"]
            output_table.add_rows(bucket_info)
            speak(output_table)

    def description(self):
        return """This plugin finds the public S3 buckets
        Created by: Dhruv Jain"""

    def add_to_output(self, bucket_info, bucket_name, status: str):
        if self.output_format == "file":
            line = bucket_name + "," + status.lower() + "\n"
            bucket_info.append(line)
        elif self.output_format == "json":
            bucket_info[status.lower()].append(bucket_name)
        elif self.output_format == "table":
            bucket_info.append([bucket_name, status])
