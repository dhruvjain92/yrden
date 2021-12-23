import boto3
from core.assistant import ask, confirm, run, speak

from core.incidents.IIResponse import IIResponse
from core.responders.aws.AWS_Functions import AWS_Functions


class accessKeyLeakage(IIResponse):
    PROP_USE_CASE = "use_case"
    QUESTION_USE_CASE = "Do you have Username (1) or Access Key ID?(2)"
    PROP_EXPLICIT_DENY = "explicit_deny"
    QUESTION_EXPLICIT_DENY = "Do you want to add explicit deny? (Default is False)"
    REQUIRED_VALUES = [
        {
            "name": PROP_USE_CASE,
            "question": QUESTION_USE_CASE,
            "value": "",
            "type": "ask",
        },
        {
            "name": PROP_EXPLICIT_DENY,
            "question": QUESTION_EXPLICIT_DENY,
            "value": False,
            "type": "confirm",
        },
    ]

    REQUIREMENTS_SATISFIED = False

    def get_requirements(self):
        return self.REQUIRED_VALUES

    def set_requirements(self, req):
        self.REQUIRED_VALUES = req

    def description(self):
        return """
        This will start access key revoke for the intended key ID or user.
        In case you selected User, all access keys and temporary credentials will be revoked.
        In case you selected Access Key ID, that access key and temporary sessions for the user will be revoked.\n
        """

    def start_response(self, aws: AWS_Functions):
        target = ""
        if self.REQUIRED_VALUES[0]["value"] == "1":
            target = ask(
                "What is the username of the person whose key you want to revoke?"
            )
            access_keys = aws.get_user_access_keys(target)
            if confirm(
                "Are you sure you want to disable the keys for " + target, "error"
            ):
                for key in access_keys["AccessKeyMetadata"]:
                    self.revoke_key(aws, key["AccessKeyId"], target)
                self.remove_older_sessions(aws, target)
                self.explicit_deny(aws, target)
            else:
                run("User cancelled the action.")
        else:
            access_key_id = ask("What is the Access Key ID?")
            speak("Finding user of the access key")
            access_key_details = aws.get_access_key_details(access_key_id)
            if access_key_details["user_name"] != "":
                run("We couldn't find the access key in our records.")
            else:
                target = access_key_details["user_name"]
                if confirm(
                    "This Access key belongs to "
                    + access_key_details["user_name"]
                    + "Please confirm the revoke."
                ):
                    self.revoke_key(aws, access_key_id, target)
                    self.remove_older_sessions(aws, target)
                    self.explicit_deny(aws, target)
                else:
                    run("User cancelled the action.")
            print(access_key_details)

    def revoke_key(self, aws: AWS_Functions, access_key_id, target):
        speak("Disabling key: " + access_key_id + " for " + target, "warning")
        aws.make_access_key_inactive(target, access_key_id)
        speak("Key has been marked inactive", "info")

    def explicit_deny(self, aws: AWS_Functions, target):
        if self.REQUIRED_VALUES[1]["value"]:
            speak("Adding explicit deny for the user", "warning")
            aws.add_explicit_deny(target)
            speak("Explicit Deny has been added to the target", "error")

    def remove_older_sessions(self, aws: AWS_Functions, target):
        speak("Removing older sessions by attaching policy", "warning")
        aws.revoke_older_sessions(target)
        speak("Older sessions have been revoked", "info")
