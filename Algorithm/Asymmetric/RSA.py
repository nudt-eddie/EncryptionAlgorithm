import random
from math import gcd

def generate_prime(bits):
    """生成一个指定位数的素数"""
    while True:
        num = random.getrandbits(bits)
        if num % 2 != 0 and is_prime(num):
            return num

def is_prime(n, k=5):
    """使用Miller-Rabin素性测试"""
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_keypair(bits):
    """生成公钥和私钥"""
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    d = pow(e, -1, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """使用公钥加密消息"""
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """使用私钥解密消息"""
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# 示例使用
if __name__ == "__main__":
    bits = 1024
    public_key, private_key = generate_keypair(bits)
    
    message = "Hello, RSA!"
    print(f"Original message: {message}")
    
    encrypted_msg = encrypt(public_key, message)
    print(f"Encrypted message: {encrypted_msg}")
    
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print(f"Decrypted message: {decrypted_msg}")

