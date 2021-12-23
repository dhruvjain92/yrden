from core.plugin.IPlugin import IPlugin
from core.assistant import *
from core.responders.aws.AWS_Functions import AWS_Functions
import importlib
from os.path import exists
import yaml
import boto3


class PlugCore:
    PLUGIN_DIR = "./plugins/"
    PLUGIN_REQ = None
    REQ_FILE = None
    OUTPUT_FORMAT = "table"

    def __init__(self, plugin_name, format, profile):
        self.PLUGIN = plugin_name
        self.OUTPUT_FORMAT = format
        boto3.setup_default_session(profile_name=profile)
        self.PLUGIN_DIR = self.PLUGIN_DIR + plugin_name + "/"
        self.REQ_FILE = self.PLUGIN_DIR + "requirements.yaml"

    def load_plugin(self):
        module_name = "plugins." + self.PLUGIN + "." + self.PLUGIN
        module = importlib.import_module(module_name)
        class_ = getattr(module, self.PLUGIN.replace("-", "_"))
        sel_plugin: IPlugin = class_(self.PLUGIN_REQ, self.OUTPUT_FORMAT)
        speak(sel_plugin.description(), "warning")
        self.check_requirements()
        sel_plugin.execute()

    def check_requirements(self):
        req_file = self.REQ_FILE
        if exists(req_file):
            with open(req_file, "r") as stream:
                try:
                    settings = yaml.safe_load(stream)["settings"]
                    for setting in settings:
                        if setting["type"] == "string":
                            setting["value"] = ask(setting["display"])
                        elif setting["type"] == "int":
                            setting["value"] = int(setting["display"])
                    self.PLUGIN_REQ = settings
                except yaml.YAMLError as exc:
                    raise Exception(exc)
        else:
            speak("No requirements file")

    def show_all_plugins():
        speak("All PLugins")
