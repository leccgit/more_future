import json
import uuid


def default_parse_uuid(o):
    if isinstance(o, uuid.UUID):
        return str(o)
    return o


result = json.dumps({"id": uuid.uuid4()}, default=default_parse_uuid)

print(result)
