from abc import ABC, abstractmethod


class IIResponse(ABC):
    @abstractmethod
    def get_requirements(self):
        pass

    @abstractmethod
    def set_requirements(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def start_response(self):
        pass
