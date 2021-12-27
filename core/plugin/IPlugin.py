from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from core.responders.aws.AWS_Functions import AWS_Functions


class IPlugin(ABC):
    requirements = None
    output_format = "table"
    output_file = ""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def description(self):
        pass

    def __init__(self, req, format, profile, output_file):
        self.requirements = req
        self.output_format = format
        self.AWS = AWS_Functions(profile)
        self.output_file = output_file

    def get_req_value(self, key):
        returnValue = None
        for setting in self.requirements:
            if setting["name"] == key:
                returnValue = setting["value"]
                break
        return returnValue

    def set_req(self, req):
        self.requirements = req

    def write_to_file(self, content):
        c_dir = self.output_file
        output_file = open("./output/" + c_dir, "a+")
        output_file.writelines(content)
        output_file.close()
        return c_dir
