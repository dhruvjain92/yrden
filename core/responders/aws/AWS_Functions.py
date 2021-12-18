import boto3


class AWS_Functions:
    AWS_PROFILE = "default"

    def __init__(self, profile):
        self.AWS_PROFILE = profile
        boto3.setup_default_session(profile_name=self.AWS_PROFILE)

    def get_user_access_keys(self, username):
        # Create IAM client
        iam = boto3.client("iam")

        # List access keys through the pagination interface.
        paginator = iam.get_paginator("list_access_keys")
        for response in paginator.paginate(UserName=username):
            print(response)
