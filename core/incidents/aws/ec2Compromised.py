import boto3
from core.assistant import ask, confirm, run, speak
from core.configuration.config import get_config

from core.incidents.IIResponse import IIResponse
from core.responders.aws.AWS_Functions import AWS_Functions


class ec2Compromised(IIResponse):
    ISOLATION_SG = get_config("aws_ec2_ir_sg")  # Please fill this
    PROP_INSTANCE_ID = "use_case"
    QUESTION_INSTANCE_ID = "What is the instance ID?"
    REQUIRED_VALUES = [
        {
            "name": PROP_INSTANCE_ID,
            "question": QUESTION_INSTANCE_ID,
            "value": "",
            "type": "ask",
        }
    ]

    REQUIREMENTS_SATISFIED = False

    def get_requirements(self):
        return self.REQUIRED_VALUES

    def set_requirements(self, req):
        self.REQUIRED_VALUES = req

    def description(self):
        return """
        This will stop the impacted instance.\n
        """

    def start_response(self, aws: AWS_Functions):
        if self.ISOLATION_SG == "":
            run(
                "Please update the config.ini with isolation security group(aws_ec2_ir_sg)"
            )
        speak("Instance Stopped", "info")
