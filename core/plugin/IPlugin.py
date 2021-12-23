from abc import ABC, abstractmethod


class IPlugin(ABC):
    # @abstractmethod
    # def get_requirements(self):
    #     pass

    # @abstractmethod
    # def set_requirements(self):
    #     pass

    # @abstractmethod
    # def description(self):
    #     pass

    # @abstractmethod
    # def credits(self):
    #     pass

    requirements = None
    output_format = "table"

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def description(self):
        pass

    def __init__(self, req, format):
        self.requirements = req
        self.output_format = format

    def get_req_value(self, key):
        returnValue = None
        for setting in self.requirements:
            if setting["name"] == key:
                returnValue = setting["value"]
                break
        return returnValue
