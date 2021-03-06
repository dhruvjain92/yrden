from core.configuration.config import get_config
from core.plugin.IPlugin import IPlugin
from core.assistant import speak, ask
import importlib
from os.path import exists
import yaml
import boto3


class PlugCore:
    PLUGIN_DIR = "./plugins/"
    PLUGIN_REQ = None
    REQ_FILE = None
    OUTPUT_FORMAT = "table"
    OUTPUT_FILE = ""

    def __init__(self, plugin_name, format, profile, output_file):
        self.PLUGIN = plugin_name
        self.OUTPUT_FORMAT = format
        self.AWS_PROFILE = profile
        # boto3.setup_default_session(profile_name=profile)
        self.PLUGIN_DIR = self.PLUGIN_DIR + plugin_name + "/"
        self.REQ_FILE = self.PLUGIN_DIR + "requirements.yaml"
        self.OUTPUT_FILE = output_file

    def load_plugin(self):
        module_name = "plugins." + self.PLUGIN + "." + self.PLUGIN
        module = importlib.import_module(module_name)
        class_ = getattr(module, self.PLUGIN.replace("-", "_"))
        sel_plugin: IPlugin = class_(
            self.PLUGIN_REQ, self.OUTPUT_FORMAT, self.AWS_PROFILE, self.OUTPUT_FILE
        )
        speak(sel_plugin.description(), "warning")
        self.check_requirements()
        sel_plugin.set_req(self.PLUGIN_REQ)
        sel_plugin.pre_execution()
        if sel_plugin.ignore_regions == False:
            regions = self.get_regions()
            for region in regions:
                speak("Setting region to " + region)
                # Set profile as empty in config if using EC2 role
                if self.AWS_PROFILE == None:
                    boto3.setup_default_session(
                    region_name=region
                )
                else:
                    boto3.setup_default_session(
                        region_name=region, profile_name=self.AWS_PROFILE
                    )
                sel_plugin.execute()
        else:
            sel_plugin.execute()
        sel_plugin.post_execution()

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

    def show_all_plugins(self):
        speak("All PLugins")

    def get_regions(self):
        regions_str = get_config("regions")
        return regions_str.split(",")
