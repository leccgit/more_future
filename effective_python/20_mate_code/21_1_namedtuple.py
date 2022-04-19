from collections import namedtuple

Record = namedtuple("device", [
    "device_code", "status_code"
], verbose=True)
rs = Record(device_code="device_1_1", status_code=1)
print(rs)
