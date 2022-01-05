from typing import TypedDict


class PluginOutputFormat(TypedDict):
    region: str
    resource_type: str
    resource_name: str
    finding: str
    additional_data: object
    comments: object


class PluginOutput:
    output_object = []

    output_format = "json"

    @property
    def dict_format(self):
        obj = {
            "region": "",
            "resource_type": "",
            "resource_name": "",
            "finding": "",
            "additional_data": {},
            "comments": {},
        }
        return obj

    def __init__(self, format):
        self.output_format = format

    def get_dict(self) -> PluginOutputFormat:
        out_var = self.dict_format.copy()
        self.output_object.append(out_var)
        return out_var

    def add_to_output(self, obj: PluginOutputFormat):
        self.output_object.append(obj)
