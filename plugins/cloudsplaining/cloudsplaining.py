import json
from core.plugin.IPlugin import IPlugin
from core.assistant import speak
import boto3
from prettytable import PrettyTable
import os
import datetime


class cloudsplaining(IPlugin):
    def execute(self):

        speak("Downloading IAM Configuration...", "warning")
        folder_name = "cloudsplaining_" + datetime.datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )
        os.system("cd output && mkdir " + folder_name)
        os.system(
            "cd output/"
            + folder_name
            + " && cloudsplaining download --profile="
            + self.aws_profile
        )
        file_name = self.aws_profile + ".json"
        speak("Configuration downloaded at ./output/" + file_name, "info")
        speak("Running analysis...", "warning")
        os.system(
            "cd output/"
            + folder_name
            + " && cloudsplaining scan --input-file "
            + file_name
        )
        speak("Analysis Completed!", "info")
        speak("You can get the report from ./output/" + folder_name + "/")

    def description(self):
        return """Cloudsplaining is an AWS IAM Security Assessment tool that identifies violations of least privilege and generates a risk-prioritized HTML report.
        Credits: https://github.com/salesforce/cloudsplaining"""

    def pre_execution(self):
        self.install_plugin_dependencies({"cloudsplaining"})
        self.output_format = None
        return super().pre_execution()
