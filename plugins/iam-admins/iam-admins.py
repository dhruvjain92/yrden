import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
import re
import pprint


class iam_admins(IPlugin):
    def execute(self):
        iam_client = boto3.client("iam")
        iam_res = boto3.resource("iam")
        # users = self.AWS.get_all_users(iam_client)
        # user_name = user["UserName"]
        user_name = "dhruv.jain"
        # user_policies = iam_client.list_user_policies(UserName=user_name)
        # for policy in user_policies:
        #     doc = iam_client.get_group_policy(GroupName='string',PolicyName='string')
        # print(user_policies)
        user = iam_res.User(user_name)
        policy_iterator = user.attached_policies.all()
        pp = pprint.PrettyPrinter(indent=4)
        for policy in policy_iterator:
            print(policy)
            pp.pprint(policy.default_version.document)

    def description(self):
        return """This plugin returns the probale sensitive files from specified S3 bucket
        Created by: Dhruv Jain"""

    def pre_execution(self):
        self.ignore_regions = True
        return super().pre_execution()
