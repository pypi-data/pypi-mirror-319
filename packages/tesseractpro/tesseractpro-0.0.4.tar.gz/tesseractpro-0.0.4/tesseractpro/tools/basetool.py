import json
from ..handle import Handle


class BaseTool:
    def __init__(self, data):
        self.data = data

    def get_id(self) -> str:
        return self.data['id']

    def get_type(self) -> str:
        return self.data['type']

    def get_option(self, key, default_value=""):
        if key not in self.data['options']:
            return default_value

        return json.loads(self.data['options'][key])

    def available_options(self) -> dict:
        return self.data['options'].keys()

    def get_handles(self):
        handles = []

        handles.append(Handle(self.data['time'], self.data['price']))

        for handle in self.data['handles']:
            handles.append(Handle(handle['time'], handle['price']))

        return handles
