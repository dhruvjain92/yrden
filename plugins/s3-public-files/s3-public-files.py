import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable
import re
import botocore
import requests
import concurrent


class s3_public_files(IPlugin):
    def execute(self):
        s3 = boto3.client("s3")
        paginator = s3.get_paginator("list_objects_v2")
        bucket_name = self.get_req_value("bucketName")
        pages = paginator.paginate(Bucket=bucket_name)
        all_objs = []
        for page in pages:
            for obj in page["Contents"]:
                all_objs.append(obj)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            res = [
                executor.submit(self.check_object_access, bucket_name, obj)
                for obj in all_objs
            ]
            concurrent.futures.wait(res)

    def check_object_access(self, bucket_name, obj):
        object_key = obj["Key"]
        config = botocore.client.Config(signature_version=botocore.UNSIGNED)
        object_url = boto3.client("s3", config=config).generate_presigned_url(
            "get_object", Params={"Bucket": bucket_name, "Key": object_key}
        )
        resp = requests.head(object_url)
        if resp.status_code == 200:
            print("Public: " + object_key)
            self.add_to_output(
                bucket_name,
                "AWS::S3",
                "Public File found: " + object_key,
                {},
                {"file_name": object_key, "file_url": object_url},
            )
        else:
            print("Private: " + object_key)

    def description(self):
        return """This plugin returns the public files from specified S3 bucket
        Created by: Dhruv Jain"""

    def pre_execution(self):
        self.ignore_regions = True
        return super().pre_execution()
