import typer
from core.assistant import *
from core.commandcenter import Command_Center


class Handler:
    def __init__(self, mode, plugin_name, format):
        if mode == "ir":
            speak("Running Incident Responder", "warning")
            self.start_ir_handler()
        elif mode == "plugin":
            speak("Running Plugin " + plugin_name, "warning")
            self.start_plugin_handler(plugin_name, format)
        else:
            run("Invalid mode selected.")

    def start_ir_handler(self):
        try:
            speak(
                "We are happy and sad to see you here. Hopefully this is just a drill.",
                "info",
            )
            cloud_provider = int(
                ask(
                    "Select your cloud provider:\n 1. AWS \n 2. Azure\nSelect Option(1 or 2)"
                )
            )
            commandcenter = Command_Center()
            if commandcenter.select_available_provider(cloud_provider) == -1:
                raise Exception("Improper input")
            if cloud_provider == commandcenter.AZURE_PROVIDER:
                run("We haven't implemented Azure functionality yet.")
            incident = self.select_incident(commandcenter.get_available_incidents())
            commandcenter.select_incident(incident)
        except Exception as e:
            run(e)

    def start_plugin_handler(self, plugin_name, format):
        commandcenter = Command_Center()
        commandcenter.load_plugin(plugin_name, format)

    def select_incident(self, incidents):
        speak("Available Incidents:")
        counter = 1
        for incident in incidents:
            speak(str(counter) + ". " + incident["display_name"])
            counter = counter + 1
        incident_index = int(ask("Select Option:"))
        incident_index = incident_index - 1
        if confirm("Please confirm", "orange"):
            speak(
                "You have selected " + incidents[incident_index]["display_name"], "info"
            )
            return incidents[incident_index]
        else:
            speak("Initiating selection again")
            return self.select_incident(incidents)
