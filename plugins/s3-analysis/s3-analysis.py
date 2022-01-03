from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3


class s3_analysis(IPlugin):
    def execute(self):
        s3 = boto3.client("s3")
        response = s3.list_buckets()
        true_val = "yes"
        false_val = "no"
        for bucket in response["Buckets"]:
            current_item = {}
            bucket_name = bucket["Name"]
            current_item["bucket"] = bucket_name
            # Checking for Server Side Encryption
            if not self.AWS.check_s3_sse(bucket_name):
                current_item["server_side_encryption"] = "disabled"
            else:
                current_item["server_side_encryption"] = "enabled"

            # Checking if bucket is public or private
            if self.AWS.check_public_bucket(bucket_name):
                current_item["public"] = true_val
            else:
                current_item["public"] = false_val

            # Checking if Versioning is Enabled
            if self.AWS.check_s3_versioning(bucket_name):
                current_item["versioning"] = true_val
            else:
                current_item["versioning"] = false_val

            # # Checking if MFA Delete is Enabled
            # if self.AWS.check_s3_mfa_delete(bucket_name):
            #     current_item["mfa_delete"] = true_val
            # else:
            #     current_item["mfa_delete"] = false_val

            # # Checking if logging is enabled
            # if self.AWS.check_s3_logging(bucket_name):
            #     current_item["logging"] = true_val
            # else:
            #     current_item["logging"] = true_val

            # # Check if lifecycle is configured
            # if self.AWS.check_s3_lifecycle(bucket_name):
            #     current_item["lifecycle"] = true_val
            # else:
            #     current_item["lifecycle"] = false_val

            # # Check if static website is configured
            # if self.AWS.check_s3_website(bucket_name):
            #     current_item["website"] = true_val
            # else:
            #     current_item["website"] = false_val

            # # Check if bucket object lock is configured
            # if self.AWS.check_s3_object_lock_mode(bucket_name):
            #     current_item["object_lock"] = true_val
            # else:
            #     current_item["object_lock"] = false_val

            self.add_to_output(
                bucket_name,
                "AWS::S3",
                "Bucket Analysis Report",
                {},
                {"analysis_report": current_item},
            )

    def description(self):
        return """This plugin analyzes the S3 buckets for security settings
        Created by: Dhruv Jain"""
