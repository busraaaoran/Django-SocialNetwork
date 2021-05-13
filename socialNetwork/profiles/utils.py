import uuid

def get_random():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code