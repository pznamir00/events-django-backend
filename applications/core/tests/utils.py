import json
from typing import Any


def errors_to_dict(errors: Any):
    return json.loads(json.dumps(errors))
