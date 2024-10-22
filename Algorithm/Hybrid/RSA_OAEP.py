import os
from math import gcd
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

def generate_keypair(bits=2048):
    key = RSA.generate(bits)
    return (key.e, key.n), (key.d, key.n)

def mgf1(seed, length, hash_func=SHA256):
    """Mask Generation Function"""
    t = b""
    hlen = hash_func.digest_size
    for counter in range(0, (length + hlen - 1) // hlen):
        c = long_to_bytes(counter, 4)
        t += hash_func.new(seed + c).digest()
    return t[:length]

def xor(data, mask):
    return bytes(a ^ b for a, b in zip(data, mask))


def oaep_pad(message, n_len, label=b"", hash_func=SHA256):
    mlen = len(message)
    hlen = hash_func.digest_size
    lhash = hash_func.new(label).digest()
    
    # Length checking
    if mlen > n_len - 2 * hlen - 2:
        raise ValueError("Message too long")
    
    ps = b"\x00" * (n_len - mlen - 2 * hlen - 2)
    db = lhash + ps + b"\x01" + message
    seed = os.urandom(hlen)
    db_mask = mgf1(seed, n_len - hlen - 1, hash_func)
    masked_db = xor(db, db_mask)
    seed_mask = mgf1(masked_db, hlen, hash_func)
    masked_seed = xor(seed, seed_mask)
    return b"\x00" + masked_seed + masked_db

def oaep_unpad(padded, n_len, label=b"", hash_func=SHA256):
    hlen = hash_func.digest_size
    lhash = hash_func.new(label).digest()
    
    # Splitting the padded message
    _, masked_seed, masked_db = padded[:1], padded[1:hlen+1], padded[hlen+1:]
    
    seed_mask = mgf1(masked_db, hlen, hash_func)
    seed = xor(masked_seed, seed_mask)
    db_mask = mgf1(seed, n_len - hlen - 1, hash_func)
    db = xor(masked_db, db_mask)
    
    _lhash = db[:hlen]
    if _lhash != lhash:
        raise ValueError("Decryption error")
    
    i = hlen
    while i < len(db):
        if db[i] == 0:
            i += 1
            continue
        elif db[i] == 1:
            i += 1
            break
        else:
            raise ValueError("Decryption error")
    
    return db[i:]

def encrypt(public_key, message, label=b""):
    e, n = public_key
    n_len = (n.bit_length() + 7) // 8
    padded = oaep_pad(message, n_len, label)
    m = bytes_to_long(padded)
    c = pow(m, e, n)
    return long_to_bytes(c, n_len)

def decrypt(private_key, ciphertext, label=b""):
    d, n = private_key
    n_len = (n.bit_length() + 7) // 8
    c = bytes_to_long(ciphertext)
    m = pow(c, d, n)
    padded = long_to_bytes(m, n_len)
    return oaep_unpad(padded, n_len, label)

# 示例使用
if __name__ == "__main__":
    # 生成密钥对
    public_key, private_key = generate_keypair()
    
    # 原始消息
    message = b"Hello, RSA-OAEP!"
    print(f"Original message: {message}")
    
    # 加密
    encrypted = encrypt(public_key, message)
    print(f"Encrypted message: {encrypted.hex()}")
    
    # 解密
    decrypted = decrypt(private_key, encrypted)
    print(f"Decrypted message: {decrypted}")
    
    # 验证
    assert decrypted == message, "Decryption failed"
    print("Encryption and decryption successful!")