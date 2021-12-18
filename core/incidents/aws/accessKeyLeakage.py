import boto3

from core.incidents.IIResponse import IIResponse
from core.responders.aws.AWS_Functions import AWS_Functions


class accessKeyLeakage(IIResponse):
    PROP_USE_CASE = "use_case"
    QUESTION_USE_CASE = "Do you have Username (1) or Access Key ID?(2)"
    PROP_EXPLICIT_DENY = "explicit_deny"
    QUESTION_EXPLICIT_DENY = "Do you want to add explicit deny? (Default is False)"
    REQUIRED_VALUES = [
        {
            "name": PROP_USE_CASE,
            "question": QUESTION_USE_CASE,
            "value": "",
            "type": "ask",
        },
        {
            "name": PROP_EXPLICIT_DENY,
            "question": QUESTION_EXPLICIT_DENY,
            "value": False,
            "type": "confirm",
        },
    ]

    REQUIREMENTS_SATISFIED = False

    def get_requirements(self):
        return self.REQUIRED_VALUES

    def set_requirements(self, req):
        self.REQUIRED_VALUES = req

    def description(self):
        return """
        This will start access key revoke for the intended key ID or user.
        In case you selected User, all access keys and temporary credentials will be revoked.
        In case you selected Access Key ID, that access key and temporary sessions for the user will be revoked.\n
        """

    def start_response(self, aws: AWS_Functions):
        aws.get_user_access_keys("dhruv.jain")
