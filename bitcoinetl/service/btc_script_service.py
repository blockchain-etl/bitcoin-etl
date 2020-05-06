import hashlib
import sys

# 58 character alphabet used
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def from_bytes (data, big_endian = False):
    if isinstance(data, str):
        data = bytearray(data)
    if big_endian:
        data = reversed(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    return num
    
def base58_encode(version, public_address):
    """
    Gets a Base58Check string
    See https://en.bitcoin.it/wiki/Base58Check_encoding
    """
    if sys.version_info.major > 2:
        version = bytes.fromhex(version)
    else:
        version = bytearray.fromhex(version)
    firstSHA256 = hashlib.sha256(version + public_address)
    secondSHA256 = hashlib.sha256(firstSHA256.digest())
    checksum = secondSHA256.digest()[:4]
    payload = version + public_address + checksum
    if sys.version_info.major > 2:
        result = int.from_bytes(payload, byteorder="big")
    else:
        result = from_bytes(payload, True)
    # count the leading 0s
    padding = len(payload) - len(payload.lstrip(b'\0'))
    encoded = []

    while result != 0:
        result, remainder = divmod(result, 58)
        encoded.append(BASE58_ALPHABET[remainder])

    return padding*"1" + "".join(encoded)[::-1]

def get_public_address(public_key):
    hash_addr = hashlib.sha256(public_key).digest()
    h = hashlib.new('ripemd160')
    h.update(hash_addr)
    public_address = h.digest()
    #print("RIPEMD-160: %s"%h.hexdigest().upper())
    return public_address

def script_asm_to_non_standard_address(script_asm): 
    #public key to bitcoin address
    public_key = bytearray.fromhex(script_asm.split(" ")[0])
    public_address = get_public_address(public_key)
    address = base58_encode("00", public_address)
    """
    script_bytes = bytearray.fromhex(script_hex)
    script_hash = hashlib.sha256(script_bytes).hexdigest()[:40]
    address = 'nonstandard' + script_hash
    """
    return address
