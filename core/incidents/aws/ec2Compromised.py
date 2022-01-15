from core.assistant import ask, confirm, run, speak
from core.configuration.config import get_config

from core.incidents.IIResponse import IIResponse
from core.responders.aws.AWS_Functions import AWS_Functions
from core.handler import Handler


class ec2Compromised(IIResponse):
    REQUIRED_VALUES = []

    REQUIREMENTS_SATISFIED = False

    def get_requirements(self):
        return self.REQUIRED_VALUES

    def set_requirements(self, req):
        pass

    def description(self):
        return ""

    def start_response(self, aws: AWS_Functions):
        Handler("plugin", "ir-ec2-compromise", "json", "")