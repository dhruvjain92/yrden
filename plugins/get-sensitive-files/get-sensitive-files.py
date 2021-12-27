import json
from core.plugin.IPlugin import IPlugin
from core.assistant import ask, speak
import boto3
from prettytable import PrettyTable
import re
from datetime import datetime


class get_sensitive_files(IPlugin):

    SENSITIVE_EXTENSION_REGEX = "\.(xml|sql|bak|ini|conf|xls|doc|xlsx|xls)$"

    def execute(self):
        s3 = boto3.client("s3")
        paginator = s3.get_paginator("list_objects_v2")
        bucket_name = self.get_req_value("bucketName")
        # bucket_name = "grofers-stage-consumer-webcdn"
        pages = paginator.paginate(Bucket=bucket_name)
        count = 0
        files = []
        if self.output_format == "json":
            files.append({"bucket_name": bucket_name, "files": []})
        for page in pages:
            for obj in page["Contents"]:
                file_name = obj["Key"]
                match = re.search(self.SENSITIVE_EXTENSION_REGEX, file_name)
                if match:
                    speak(file_name)
                    if self.output_format == "file":
                        files.append(bucket_name + ":" + file_name + "\n")
                    elif self.output_format == "json":
                        files[0]["files"].append(file_name)
                    else:
                        files.append([bucket_name, file_name])
                    count = count + 1
        speak(str(count) + " files found.", "info")
        if self.output_format == "json":
            speak(json.dumps(files, indent=2, sort_keys=True))
        elif self.output_format == "file":
            self.write_to_file(files)
        else:
            output_table = PrettyTable()
            output_table.field_names = ["Bucket", "Files"]
            output_table.add_rows(files)
            speak(output_table)

    def description(self):
        return """This plugin returns the probale sensitive files from specified S3 bucket
        Created by: Dhruv Jain"""
