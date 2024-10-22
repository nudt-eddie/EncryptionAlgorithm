class PlayfairCipher:
    def __init__(self, key):
        self.key = self.prepare_key(key)
        self.matrix = self.generate_matrix()

    def prepare_key(self, key):
        key = key.upper().replace("J", "I")
        return "".join(dict.fromkeys(key + "ABCDEFGHIKLMNOPQRSTUVWXYZ"))

    def generate_matrix(self):
        return [list(self.key[i:i+5]) for i in range(0, 25, 5)]

    def find_position(self, letter):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == letter:
                    return i, j
        return -1, -1

    def encrypt_pair(self, a, b):
        row1, col1 = self.find_position(a)
        row2, col2 = self.find_position(b)

        if row1 == row2:
            return self.matrix[row1][(col1+1)%5], self.matrix[row2][(col2+1)%5]
        elif col1 == col2:
            return self.matrix[(row1+1)%5][col1], self.matrix[(row2+1)%5][col2]
        else:
            return self.matrix[row1][col2], self.matrix[row2][col1]

    def decrypt_pair(self, a, b):
        row1, col1 = self.find_position(a)
        row2, col2 = self.find_position(b)

        if row1 == row2:
            return self.matrix[row1][(col1-1)%5], self.matrix[row2][(col2-1)%5]
        elif col1 == col2:
            return self.matrix[(row1-1)%5][col1], self.matrix[(row2-1)%5][col2]
        else:
            return self.matrix[row1][col2], self.matrix[row2][col1]

    def prepare_text(self, text):
        text = text.upper().replace("J", "I")
        result = []
        i = 0
        while i < len(text):
            if i == len(text) - 1 or text[i] == text[i+1]:
                result.extend([text[i], 'X'])
                i += 1
            else:
                result.extend([text[i], text[i+1]])
                i += 2
        return "".join(result)

    def encrypt(self, plaintext):
        plaintext = self.prepare_text(plaintext)
        ciphertext = ""
        for i in range(0, len(plaintext), 2):
            a, b = self.encrypt_pair(plaintext[i], plaintext[i+1])
            ciphertext += a + b
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ""
        for i in range(0, len(ciphertext), 2):
            a, b = self.decrypt_pair(ciphertext[i], ciphertext[i+1])
            plaintext += a + b
        return plaintext.replace("X", "")

# 示例使用
if __name__ == "__main__":
    key = "KEYWORD"
    playfair = PlayfairCipher(key)

    message = "Hello, Playfair Cipher!"
    print(f"Original message: {message}")

    encrypted = playfair.encrypt(message)
    print(f"Encrypted message: {encrypted}")

    decrypted = playfair.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
