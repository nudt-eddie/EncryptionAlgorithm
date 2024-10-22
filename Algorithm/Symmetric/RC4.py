class RC4:
    def __init__(self, key):
        self.key = key
        self.S = list(range(256))
        self.initialize_state()

    def initialize_state(self):
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def generate_keystream(self, length):
        i = j = 0
        keystream = []
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[(self.S[i] + self.S[j]) % 256]
            keystream.append(K)
        return keystream

    def encrypt(self, plaintext):
        keystream = self.generate_keystream(len(plaintext))
        ciphertext = bytearray()
        for p, k in zip(plaintext, keystream):
            c = p ^ k
            ciphertext.append(c)
        return bytes(ciphertext)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)  # RC4的加密和解密过程相同

def rc4_encrypt(key, plaintext):
    cipher = RC4([ord(c) for c in key])
    return cipher.encrypt(plaintext.encode('utf-8'))

def rc4_decrypt(key, ciphertext):
    cipher = RC4([ord(c) for c in key])
    return cipher.decrypt(ciphertext).decode('utf-8')

# 示例使用
if __name__ == "__main__":
    key = "SecretKey123"
    message = "Hello, RC4 encryption!"
    print(f"Original message: {message}")

    encrypted = rc4_encrypt(key, message)
    print(f"Encrypted message: {encrypted.hex()}")

    decrypted = rc4_decrypt(key, encrypted)
    print(f"Decrypted message: {decrypted}")

