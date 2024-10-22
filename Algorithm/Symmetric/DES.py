# DES Constants
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

def permute(block, table):
    return [block[i - 1] for i in table]

def string_to_bit_array(text):
    return [int(bit) for byte in text for bit in f'{byte:08b}']

def bit_array_to_string(array):
    return bytes(int(''.join(map(str, array[i:i+8])), 2) for i in range(0, len(array), 8))

def generate_subkeys(key):
    # 这里应该实现子密钥生成
    # 为简化，我们只返回一个示例子密钥
    return [key] * 16

def f_function(right, subkey):
    # 扩展置换
    expanded = permute(right, E)
    # XOR with subkey
    xored = [a ^ b for a, b in zip(expanded, subkey)]
    # S-box substitution
    substituted = []
    for i in range(8):
        block = xored[i*6:(i+1)*6]
        row = int(f"{block[0]}{block[5]}", 2)
        col = int(''.join(map(str, block[1:5])), 2)
        substituted.extend(f'{S_BOXES[i][row][col]:04b}')
    # Permutation
    return permute(substituted, P)

def des_round(left, right, subkey):
    f_result = f_function(right, subkey)
    new_right = [int(l) ^ int(r) for l, r in zip(left, f_result)]
    return right, new_right

def pad(text):
    """使用PKCS7填充"""
    padding_length = 8 - (len(text) % 8)
    padding = bytes([padding_length] * padding_length)
    return text.encode('utf-8') + padding

def unpad(padded_text):
    """移除PKCS7填充"""
    padding_length = padded_text[-1]
    return padded_text[:-padding_length].decode('utf-8')

class DESCipher:
    def __init__(self, key):
        self.subkeys = generate_subkeys(string_to_bit_array(pad(key)[:8]))

    def encrypt(self, plaintext):
        padded_text = pad(plaintext)
        ciphertext = b''
        for i in range(0, len(padded_text), 8):
            block = padded_text[i:i+8]
            block = string_to_bit_array(block)
            block = permute(block, IP)
            left, right = block[:32], block[32:]
            for i in range(16):
                left, right = des_round(left, right, self.subkeys[i])
            block = right + left
            block = permute(block, FP)
            ciphertext += bit_array_to_string(block)
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            block = string_to_bit_array(block)
            block = permute(block, IP)
            left, right = block[:32], block[32:]
            for i in range(15, -1, -1):
                left, right = des_round(left, right, self.subkeys[i])
            block = right + left
            block = permute(block, FP)
            plaintext += bit_array_to_string(block)
        return unpad(plaintext)

# 示例使用
if __name__ == "__main__":
    key = "mysecret"
    des = DESCipher(key)

    message = "Hello, DES encryption with padding!"
    print(f"Original message: {message}")

    encrypted = des.encrypt(message)
    print(f"Encrypted message: {encrypted.hex()}")

    decrypted = des.decrypt(encrypted)
    print(f"Decrypted message: {decrypted}")
