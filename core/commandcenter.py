import yaml

from core.assistant import ask
from core.configuration.config import get_config
from core.plugin.plugcore import PlugCore
from core.responders.aws.aws import AWS_Responder


class Command_Center:

    AZURE_PROVIDER = 2
    AWS_PROVIDER = 1
    SELECTED_PROVIDER = -1
    IR_LIST = "./core/incidents/list.yaml"

    def __init__(self):
        self.SELECTED_PROVIDER = 1

    def select_available_provider(self, provider: int):
        if provider in (self.AZURE_PROVIDER, self.AWS_PROVIDER):
            self.SELECTED_PROVIDER = provider
        return self.SELECTED_PROVIDER

    def get_available_incidents(self):
        self.check_provider()
        shortlisted_incidents = None
        with open(self.IR_LIST, "r") as stream:
            try:
                incidents_list = yaml.safe_load(stream)["incidents"]
                if self.SELECTED_PROVIDER == self.AZURE_PROVIDER:
                    shortlisted_incidents = incidents_list["azure"]
                elif self.SELECTED_PROVIDER == self.AWS_PROVIDER:
                    shortlisted_incidents = incidents_list["aws"]
            except yaml.YAMLError as exc:
                raise Exception(exc)
        return shortlisted_incidents

    def select_incident(self, incident):
        AWS_Responder(incident)

    def check_provider(self):
        if self.SELECTED_PROVIDER == -1:
            raise Exception("No provider selected")

    def load_plugin(self, plugin_name: str, format: str, output_file: str):
        plugin_arr = plugin_name.split(",")
        profile = get_config("default_profile")
        if profile == "":
            profile = None
        for plugin in plugin_arr:
            plugcore = PlugCore(plugin, format, profile, output_file)
            plugcore.load_plugin()
