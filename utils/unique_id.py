import secrets

def generate_unique_id(length):
    return secrets.token_hex(length)
