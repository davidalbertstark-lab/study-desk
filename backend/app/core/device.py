import uuid

def get_or_create_device_id(device_id: str | None) -> str:
    if device_id:
        return device_id
    return str(uuid.uuid4())