from importlib import import_module
import importlib
from importlib.util import find_spec
import sys
from core.assistant import *
import boto3
from core.incidents.IIResponse import IIResponse

from core.responders.aws.AWS_Functions import AWS_Functions


class AWS_Responder:
    AWS = None

    def __init__(self, incident):
        module_name = "core.incidents.aws." + incident["file"]
        module = importlib.import_module(module_name)
        class_ = getattr(module, incident["file"])
        instance: IIResponse = class_()
        self.set_profile()
        self.run_ir(instance)

    def set_profile(self):
        self.AWS = AWS_Functions(ask("Select your AWS profile", "warning"))

    def run_ir(self, instance: IIResponse):
        self.ir_requirements(instance)
        speak(instance.description(), "warning")
        instance.start_response(self.AWS)

    def ir_requirements(self, incident_response: IIResponse):
        requirements = incident_response.get_requirements()
        for req in requirements:
            if req["type"] == "ask":
                req["value"] = ask(req["question"])
            if req["type"] == "confirm":
                req["value"] = confirm(req["question"])
        incident_response.set_requirements(requirements)
        return incident_response
