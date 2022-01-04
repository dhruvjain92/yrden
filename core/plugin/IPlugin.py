from abc import ABC, abstractmethod
import json

from prettytable.prettytable import PrettyTable
from core.assistant import speak
from core.plugin.pluginoutput import PluginOutput
from core.responders.aws.AWS_Functions import AWS_Functions
import boto3
import sys
import subprocess
import pkg_resources


class IPlugin(ABC):
    requirements = None
    output_format = "table"
    output_file = ""
    aws_profile = ""
    output_content = []

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
        self.aws_profile = profile
        self.output_file = output_file
        self.plugin_output = PluginOutput(format)

    def get_req_value(self, key):
        returnValue = None
        for setting in self.requirements:
            if setting["name"] == key:
                returnValue = setting["value"]
                break
        return returnValue

    def set_req(self, req):
        self.requirements = req

    def write_to_file(self, content, extension=""):
        c_dir = self.output_file + extension
        output_file = open("./output/" + c_dir, "a+")
        output_file.writelines(content)
        output_file.close()
        return c_dir

    def get_aws_region(self):
        client = boto3.client("s3")  # example client, could be any
        return client.meta.region_name

    def show_results(self):
        pl_output = self.plugin_output.output_object
        if self.output_format == "file":
            self.write_to_file(json.dumps(pl_output))
            pl_output = "Written to" + "./output/" + self.output_file
        elif self.output_format == "table":
            output_table = PrettyTable()
            headers = []
            for key in self.plugin_output.dict_format:
                headers.append(key)
            output_table.field_names = headers
            rows = []
            for item in pl_output:
                row = []
                for key in self.plugin_output.dict_format:
                    row.append(item[key])
                rows.append(row)
            output_table.add_rows(rows)
            pl_output = output_table
        elif self.output_format == "csv":
            headers = []
            for key in self.plugin_output.dict_format:
                headers.append(key)
            lines = (",").join(headers) + "\n"
            for item in pl_output:
                row = []
                for key in self.plugin_output.dict_format:
                    row.append(item[key])
                lines = lines + (",").join(row) + "\n"
            self.write_to_file(lines, ".csv")
            pl_output = "Written to" + "./output/" + self.output_file + ".csv"
        elif self.output_format == None:
            pl_output = None
        return pl_output

    def add_to_output(
        self,
        resource_name: str,
        resource_type: str,
        finding: str,
        comments: str = {},
        additional_data={},
    ):
        row = self.plugin_output.get_dict()
        row["region"] = self.get_aws_region()
        row["resource_name"] = resource_name
        row["resource_type"] = resource_type
        row["finding"] = finding
        row["comments"] = json.dumps(comments)
        row["additional_data"] = json.dumps(additional_data)

    # Returns back the results on the basis of output format selection
    # You can override this function to change post execution steps in your plugin
    def post_execution(self):
        results = self.show_results()
        if not results == None:
            speak(self.show_results())

    # You can override this function to change pre execution steps in your plugin
    def pre_execution(self):
        pass

    def install_plugin_dependencies(self, pip_req_set):
        speak("Installing missing dependencies...", "warning")
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = pip_req_set - installed
        if missing:
            python = sys.executable
            subprocess.check_call(
                [python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL
            )
            speak("Dependencies Installed!", "info")
        else:
            speak("Dependencies already Installed!", "info")
