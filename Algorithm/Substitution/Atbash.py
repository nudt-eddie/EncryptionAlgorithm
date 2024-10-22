class AtbashCipher:
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.reverse_alphabet = self.alphabet[::-1]

    def encrypt(self, plaintext):
        ciphertext = ""
        for char in plaintext.upper():
            if char in self.alphabet:
                index = self.alphabet.index(char)
                ciphertext += self.reverse_alphabet[index]
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)  # Atbash加密和解密是相同的操作

# 示例使用
if __name__ == "__main__":
    atbash = AtbashCipher()

    message = "Hello, Atbash Cipher!"
    print(f"Original message: {message}")

    encrypted = atbash.encrypt(message)
    print(f"Encrypted message: {encrypted}")

    decrypted = atbash.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
