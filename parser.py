import json
import re

def parse_batch_response(raw: str, expected_count: int):
    cleaned = re.sub(r"^```(json)?", "", raw.strip())
    cleaned = re.sub(r"```$", "", cleaned)

    try:
        data = json.loads(cleaned)
        if not isinstance(data, list):
            raise ValueError("Not a list")
        if len(data) != expected_count:
            raise ValueError("Count mismatch")
        return data
    except Exception as e:
        raise ValueError(f"Parse failed: {e}\nRaw: {cleaned[:200]}")