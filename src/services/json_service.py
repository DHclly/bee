import json


def serialize(data,pretty=False,ensure_ascii=False):
    return json.dumps(data,indent=4 if pretty else None,ensure_ascii=ensure_ascii)

def deserialize(data):
    return json.loads(data)