class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper()

    def encrypt(self, plaintext):
        ciphertext = ""
        key_index = 0
        for char in plaintext.upper():
            if char.isalpha():
                # 计算位移
                shift = ord(self.key[key_index % len(self.key)]) - ord('A')
                # 加密字符
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext += encrypted_char
                key_index += 1
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""
        key_index = 0
        for char in ciphertext.upper():
            if char.isalpha():
                # 计算位移
                shift = ord(self.key[key_index % len(self.key)]) - ord('A')
                # 解密字符
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                plaintext += decrypted_char
                key_index += 1
            else:
                plaintext += char
        return plaintext

# 示例使用
if __name__ == "__main__":
    key = "KEY"
    vigenere = VigenereCipher(key)

    message = "Hello, Vigenere Cipher!"
    print(f"Original message: {message}")

    encrypted = vigenere.encrypt(message)
    print(f"Encrypted message: {encrypted}")

    decrypted = vigenere.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
