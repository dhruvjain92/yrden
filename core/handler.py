import typer
from core.assistant import *
from core.commandcenter import Command_Center


class Handler:
    def __init__(self):
        try:
            speak(
                "We are happy and sad to see you here. Hopefully this is just a drill.",
                "info",
            )
            cloud_provider = int(
                ask(
                    "Select your cloud provider:\n 1. Azure \n 2. AWS\nSelect Option(1 or 2)"
                )
            )
            commandcenter = Command_Center()
            if commandcenter.select_available_provider(cloud_provider) == -1:
                raise Exception("Improper input")
            incident = self.select_incident(commandcenter.get_available_incidents())
            commandcenter.select_incident(incident)
            print(incident)
        except Exception as e:
            run(e)

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
