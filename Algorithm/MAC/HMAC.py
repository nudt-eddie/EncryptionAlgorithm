import hashlib

def hmac(key, message, hash_func='sha256'):
    """
    实现HMAC算法
    :param key: 密钥
    :param message: 要认证的消息
    :param hash_func: 使用的哈希函数（默认为SHA-256）
    :return: HMAC值
    """
    block_size = 64  # 对于SHA-256，块大小为64字节

    # 如果密钥长度大于块大小，先进行哈希
    if len(key) > block_size:
        key = hashlib.new(hash_func, key).digest()

    # 如果密钥长度小于块大小，用0填充
    if len(key) < block_size:
        key = key + b'\x00' * (block_size - len(key))

    # 准备内部和外部填充
    o_key_pad = bytes(x ^ 0x5c for x in key)
    i_key_pad = bytes(x ^ 0x36 for x in key)

    # 内部哈希
    inner_hash = hashlib.new(hash_func, i_key_pad + message.encode('utf-8')).digest()

    # 外部哈希
    return hashlib.new(hash_func, o_key_pad + inner_hash).hexdigest()

# 示例使用
if __name__ == "__main__":
    key = "secret_key"
    message = "Hello, HMAC!"
    
    print(f"Key: {key}")
    print(f"Message: {message}")
    
    hmac_sha256 = hmac(key.encode('utf-8'), message)
    print(f"HMAC-SHA256: {hmac_sha256}")

    # 使用不同的哈希函数
    hmac_sha512 = hmac(key.encode('utf-8'), message, 'sha512')
    print(f"HMAC-SHA512: {hmac_sha512}")

    # 验证HMAC
    def verify_hmac(key, message, hmac_value, hash_func='sha256'):
        return hmac(key, message, hash_func) == hmac_value

    is_valid = verify_hmac(key.encode('utf-8'), message, hmac_sha256)
    print(f"HMAC verification: {'Success' if is_valid else 'Failed'}")

    # 尝试验证被篡改的消息
    tampered_message = "Hello, Tampered HMAC!"
    is_valid = verify_hmac(key.encode('utf-8'), tampered_message, hmac_sha256)
    print(f"Tampered message HMAC verification: {'Success' if is_valid else 'Failed'}")
