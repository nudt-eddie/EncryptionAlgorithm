class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift % 26

    def encrypt(self, plaintext):
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - ascii_offset + self.shift) % 26
                ciphertext += chr(shifted + ascii_offset)
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - ascii_offset - self.shift) % 26
                plaintext += chr(shifted + ascii_offset)
            else:
                plaintext += char
        return plaintext

# 示例使用
if __name__ == "__main__":
    shift = 3  # 经典的凯撒加密使用3作为位移
    caesar = CaesarCipher(shift)

    message = "Hello, Caesar Cipher!"
    print(f"Original message: {message}")

    encrypted = caesar.encrypt(message)
    print(f"Encrypted message: {encrypted}")

    decrypted = caesar.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
