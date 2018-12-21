import hashlib


def script_hex_to_non_standard_address(script_hex):
    if script_hex is None:
        script_hex = ''

    script_bytes = bytearray.fromhex(script_hex)
    script_hash = hashlib.sha256(script_bytes).hexdigest()[:40]
    address = 'nonstandard' + script_hash
    return address
