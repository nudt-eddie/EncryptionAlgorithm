import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class ECIES:
    def __init__(self, curve=ec.SECP256R1()):
        self.curve = curve

    def generate_key_pair(self):
        private_key = ec.generate_private_key(self.curve, default_backend())
        public_key = private_key.public_key()
        return private_key, public_key

    def encrypt(self, public_key, plaintext):
        # 生成临时密钥对
        ephemeral_private_key = ec.generate_private_key(self.curve, default_backend())
        ephemeral_public_key = ephemeral_private_key.public_key()

        # 计算共享密钥
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)

        # 使用KDF派生加密密钥和MAC密钥
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=None,
            info=b'ECIES',
            backend=default_backend()
        ).derive(shared_key)

        enc_key = derived_key[:32]
        mac_key = derived_key[32:]

        # 使用AES-GCM加密消息
        iv = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(enc_key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        tag = encryptor.tag

        # 序列化临时公钥
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        serialized_ephemeral_public_key = ephemeral_public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.CompressedPoint
        )

        return serialized_ephemeral_public_key + iv + ciphertext + tag

    def decrypt(self, private_key, ciphertext):
        # 反序列化临时公钥
        key_size = (private_key.curve.key_size + 7) // 8 + 1
        serialized_ephemeral_public_key = ciphertext[:key_size]
        ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
            private_key.curve,
            serialized_ephemeral_public_key
        )

        # 计算共享密钥
        shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)

        # 使用KDF派生加密密钥和MAC密钥
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=None,
            info=b'ECIES',
            backend=default_backend()
        ).derive(shared_key)

        enc_key = derived_key[:32]
        mac_key = derived_key[32:]

        # 解密消息
        iv = ciphertext[key_size:key_size+12]
        tag = ciphertext[-16:]
        encrypted_data = ciphertext[key_size+12:-16]

        decryptor = Cipher(
            algorithms.AES(enc_key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()

        return decryptor.update(encrypted_data) + decryptor.finalize()

# 示例使用
if __name__ == "__main__":
    ecies = ECIES()

    # 生成密钥对
    private_key, public_key = ecies.generate_key_pair()

    # 加密消息
    message = b"Hello, ECIES!"
    print("Original message: ", message)
        
    # 加密
    encrypted = ecies.encrypt(public_key, message)
    print(f"Encrypted message: {encrypted.hex()}")

    # 解密消息
    decrypted = ecies.decrypt(private_key, encrypted)
    print(f"Decrypted message: {decrypted.decode()}")

    # 验证
    assert decrypted == message, "Decryption failed"
    print("Encryption and decryption successful!")
