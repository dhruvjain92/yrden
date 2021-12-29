import boto3
from datetime import datetime
import botocore
import typer
from core.configuration.config import check_test_mode
import json


class AWS_Functions:
    aws_profile = "default"
    test_mode = False

    def __init__(self, profile):
        self.aws_profile = profile
        self.test_mode = check_test_mode()
        boto3.setup_default_session(profile_name=self.aws_profile)

    def get_user_access_keys(self, username):
        iam = boto3.client("iam")
        paginator = iam.get_paginator("list_access_keys")
        result = {}
        for response in paginator.paginate(UserName=username):
            result = response
        return result

    def make_access_key_inactive(self, username, key_id):
        if not self.test_mode:
            iam = boto3.client("iam")
            iam.update_access_key(
                UserName=username, AccessKeyId=key_id, Status="Inactive"
            )

    def revoke_older_sessions(self, username):
        if not self.test_mode:
            iam = boto3.client("iam")
            current_time = datetime.utcnow().isoformat()
            revoke_policy_json = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Deny",
                        "Action": ["*"],
                        "Resource": ["*"],
                        "Condition": {
                            "DateLessThan": {"aws:TokenIssueTime": current_time}
                        },
                    }
                ],
            }
            policy_name = "RevokePolicy-" + str(datetime.now().timestamp())
            iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(revoke_policy_json),
            )
            account_id = boto3.client("sts").get_caller_identity().get("Account")
            try:
                iam.attach_role_policy(
                    PolicyArn="arn:aws:iam::" + account_id + ":policy/" + policy_name,
                    RoleName=username,
                )
            except Exception as e:
                iam.attach_user_policy(
                    PolicyArn="arn:aws:iam::" + account_id + ":policy/" + policy_name,
                    UserName=username,
                )

    def add_explicit_deny(self, username):
        if not self.test_mode:
            iam = boto3.client("iam")
            revoke_policy_json = {
                "Version": "2012-10-17",
                "Statement": [{"Effect": "Deny", "Action": ["*"], "Resource": ["*"]}],
            }
            policy_name = "ExplicitDeny-" + str(datetime.now().timestamp())
            iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(revoke_policy_json),
            )
            account_id = boto3.client("sts").get_caller_identity().get("Account")
            iam.attach_role_policy(
                PolicyArn="arn:aws:iam::" + account_id + ":policy/" + policy_name,
                RoleName=username,
            )

    def get_access_key_details(self, access_key_id):
        access_key_details = {}
        access_key_details["user_name"] = ""
        if not self.test_mode:
            iam = boto3.client("iam")
            users = []
            pages = self.get_all_users(iam)
            for page in pages:
                users = users + page["Users"]
            with typer.progressbar(users) as progress:
                for sel_user in progress:
                    user = sel_user["UserName"]
                    keys = iam.list_access_keys(UserName=user)
                    if user == "lakshya.rawat":
                        print(keys)
                    for key in keys["AccessKeyMetadata"]:
                        if key["AccessKeyId"] == access_key_id:
                            access_key_details["user_name"] = key["UserName"]
                            access_key_details["status"] = key["Status"]
                            access_key_details["create_date"] = key["CreateDate"]
                            break
                    if access_key_details["user_name"] != "":
                        break
        return access_key_details

    def get_all_users(self, iam):
        paginator = iam.get_paginator("list_users")
        return paginator.paginate()

    def check_public_bucket(self, bucket_name):
        client = boto3.client("s3")
        bucket_public = False
        try:
            response = client.get_public_access_block(Bucket=bucket_name)
            if not (
                response["PublicAccessBlockConfiguration"]["BlockPublicAcls"]
                and response["PublicAccessBlockConfiguration"]["BlockPublicPolicy"]
            ):
                bucket_public = True
        except botocore.exceptions.ClientError as e:
            bucket_public = False
        if not bucket_public:
            try:
                response = client.get_bucket_policy_status(Bucket=bucket_name)
                bucket_public = response["PolicyStatus"]["IsPublic"]
            except botocore.exceptions.ClientError as e:
                bucket_public = False
        if not bucket_public:
            grants = client.get_bucket_acl(Bucket=bucket_name).get("Grants")
            for grant in grants:
                if (
                    grant["Grantee"]["Type"] == "CanonicalUser"
                    and "DisplayName" in grant["Grantee"]
                    and "All Users" in grant["Grantee"]["DisplayName"]
                ):
                    bucket_public = True
        return bucket_public

    def check_s3_versioning(self, bucket_name):
        s3client = boto3.client("s3")
        response = s3client.get_bucket_versioning(Bucket=bucket_name)
        versioning_enabled = False
        if "Status" in response and response["Status"] == "Enabled":
            versioning_enabled = True
        return versioning_enabled
