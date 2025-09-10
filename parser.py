import json

def parse_batch_response(raw: str, expected_count: int):
    try:
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Not a list")
        if len(data) != expected_count:
            raise ValueError("Count mismatch")
        return data
    except Exception as e:
        raise ValueError(f"Parse failed: {e}\nRaw: {raw[:200]}")