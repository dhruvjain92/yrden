import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable
import re


class get_sensitive_files(IPlugin):

    SENSITIVE_EXTENSION_REGEX = "\.(xml|sql|bak|ini|conf|xls|doc|xlsx|xls)$"

    def execute(self):
        s3 = boto3.client("s3")
        paginator = s3.get_paginator("list_objects_v2")
        bucket_name = self.get_req_value("bucketName")
        pages = paginator.paginate(Bucket=bucket_name)
        count = 0
        for page in pages:
            for obj in page["Contents"]:
                file_name = obj["Key"]
                match = re.search(self.SENSITIVE_EXTENSION_REGEX, file_name)
                if match:
                    speak(file_name)
                    self.add_to_output(
                        bucket_name,
                        "AWS::S3",
                        "Sensitive File found: " + file_name,
                        {},
                        {"file_name": file_name},
                    )
                    count = count + 1
        speak(str(count) + " files found.", "info")

    def description(self):
        return """This plugin returns the probale sensitive files from specified S3 bucket
        Created by: Dhruv Jain"""

    def pre_execution(self):
        self.ignore_regions = True
        return super().pre_execution()
