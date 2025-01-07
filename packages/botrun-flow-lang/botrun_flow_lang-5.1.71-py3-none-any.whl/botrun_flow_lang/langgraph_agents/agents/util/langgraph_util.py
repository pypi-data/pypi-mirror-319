import json
from typing import Dict


def event_to_json(event: Dict):
    messages = event.get("data", {}).get("input", {}).get("messages", [])
    return json.dumps(event, ensure_ascii=False)
