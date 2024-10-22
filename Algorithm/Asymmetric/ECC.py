from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# 生成ECC密钥对
def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key

# 使用ECC公钥加密字符串
def encrypt_message(message, public_key):
    # 生成一个随机的临时密钥对
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # 计算共享密钥
    shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)

    # 使用HKDF从共享密钥派生对称密钥
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # 使用对称密钥加密消息
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    # 返回加密后的消息和临时公钥
    return ephemeral_public_key, iv, ciphertext

# 使用ECC私钥解密字符串
def decrypt_message(ephemeral_public_key, iv, ciphertext, private_key):
    # 计算共享密钥
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    # 使用HKDF从共享密钥派生对称密钥
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)

    # 使用对称密钥解密消息
    cipher = Cipher(algorithms.AES(derived_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()

# 示例使用
if __name__ == "__main__":
    # 生成ECC密钥对
    private_key, public_key = generate_ecc_keys()

    # 要加密的消息
    message = "Hello, ECC!"
    print(f"Original Message: {message}")
    
    # 加密消息
    ephemeral_public_key, iv, ciphertext = encrypt_message(message, public_key)
    print(f"Encrypted Message: {ciphertext}")

    # 解密消息
    decrypted_message = decrypt_message(ephemeral_public_key, iv, ciphertext, private_key)
    print(f"Decrypted Message: {decrypted_message}")