from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def leftshift(data):
    return (int.from_bytes(data, 'big') << 1).to_bytes(len(data), 'big')

def generate_subkeys(key):
    cipher = AES.new(key, AES.MODE_ECB)
    L = cipher.encrypt(b'\x00' * 16)

    if L[0] & 0x80:
        K1 = xor_bytes(leftshift(L), b'\x87')
    else:
        K1 = leftshift(L)

    if K1[0] & 0x80:
        K2 = xor_bytes(leftshift(K1), b'\x87')
    else:
        K2 = leftshift(K1)

    return K1, K2

def pad(message):
    if len(message) % 16 == 0:
        return message + b'\x80' + b'\x00' * 15
    else:
        return message + b'\x80' + b'\x00' * (15 - (len(message) % 16))

def cmac(key, message):
    K1, K2 = generate_subkeys(key)
    cipher = AES.new(key, AES.MODE_ECB)

    if len(message) == 0:
        padded_message = b'\x80' + b'\x00' * 15
        return cipher.encrypt(xor_bytes(padded_message, K2))

    if len(message) % 16 == 0:
        last_block = message[-16:]
        rest = message[:-16]
        last_block = xor_bytes(last_block, K1)
    else:
        padded_message = pad(message)
        last_block = padded_message[-16:]
        rest = padded_message[:-16]
        last_block = xor_bytes(last_block, K2)

    X = b'\x00' * 16
    for i in range(0, len(rest), 16):
        block = rest[i:i+16]
        X = cipher.encrypt(xor_bytes(X, block))

    Y = cipher.encrypt(xor_bytes(X, last_block))
    return Y

def verify_cmac(key, message, tag):
    return cmac(key, message) == tag

# 示例使用
if __name__ == "__main__":
    key = get_random_bytes(16)  # 128-bit key for AES
    message = b"Hello, CMAC!"

    print(f"Key: {key.hex()}")
    print(f"Message: {message}")

    tag = cmac(key, message)
    print(f"CMAC: {tag.hex()}")

    # 验证CMAC
    is_valid = verify_cmac(key, message, tag)
    print(f"CMAC verification: {'Success' if is_valid else 'Failed'}")

    # 尝试验证被篡改的消息
    tampered_message = b"Hello, CMAC?"
    is_valid = verify_cmac(key, tampered_message, tag)
    print(f"Tampered message CMAC verification: {'Success' if is_valid else 'Failed'}")
