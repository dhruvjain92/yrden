from core.plugin.IPlugin import IPlugin
from core.assistant import speak


class disable_old_keys(IPlugin):
    def execute(self):
        speak("CHecking for older keys")

    def description(self):
        return ""
