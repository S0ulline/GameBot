import json


class Payload(object):
    def __init__(self, data_json_string):
        self.__dict__ = json.loads(data_json_string)
