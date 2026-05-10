KEY = b"mysecretkey12345"

def xor(data):
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ KEY[i % len(KEY)])
    return bytes(result)
