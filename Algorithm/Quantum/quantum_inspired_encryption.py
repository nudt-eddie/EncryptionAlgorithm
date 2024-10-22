import random
import math

def generate_key(length):
    """生成一个随机的量子态序列作为密钥"""
    return [random.choice(['0', '1', '+', '-']) for _ in range(length)]

def measure_qubit(qubit, basis):
    """模拟量子测量"""
    if basis == qubit:
        return qubit
    elif qubit in ['0', '1'] and basis in ['+', '-']:
        return random.choice(['0', '1'])
    elif qubit in ['+', '-'] and basis in ['0', '1']:
        return random.choice(['+', '-'])

def encrypt(message, key):
    """使用量子密钥加密消息"""
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    encrypted = []
    for bit, qubit in zip(binary_message, key):
        if bit == '0':
            encrypted.append(qubit)
        else:
            encrypted.append('+' if qubit in ['0', '-'] else '-' if qubit == '+' else '0')
    return encrypted

def decrypt(encrypted, key):
    """使用量子密钥解密消息"""
    decrypted_binary = ''
    for enc_qubit, key_qubit in zip(encrypted, key):
        if enc_qubit == key_qubit:
            decrypted_binary += '0'
        else:
            decrypted_binary += '1'
    
    # 将二进制转换回字符串
    decrypted = ''.join(chr(int(decrypted_binary[i:i+8], 2)) for i in range(0, len(decrypted_binary), 8))
    return decrypted

# 使用示例
message = "Hello, Quantum World!"
key = generate_key(len(message) * 8)  # 每个字符需要8位
encrypted = encrypt(message, key)
decrypted = decrypt(encrypted, key)

print(f"原始消息: {message}")
print(f"加密后: {''.join(encrypted)}")
print(f"解密后: {decrypted}")
