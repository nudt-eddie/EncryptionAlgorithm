import random
import hashlib

def mod_inverse(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        return None  # Changed to return None instead of raising an exception
    else:
        return x % m

class DSA:
    def __init__(self, p=None, q=None, g=None):
        if p is None or q is None or g is None:
            # 使用预定义的参数（这只是一个例子，实际应用中应使用更大的参数）
            self.p = 0xfced6b33717939c0e7d2ea46d1fdc0a2a1f7e1d2d62a1330d1b0d4f5f8f5b8d7
            self.q = 0xd5f3f9284d8a70a7e1b6e789c9e1c2d3
            self.g = 0x7a36d88b1c9957e2d3c9e6d7f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0
        else:
            self.p = p
            self.q = q
            self.g = g

    def generate_keypair(self):
        x = random.randint(1, self.q - 1)
        y = pow(self.g, x, self.p)
        return (x, y)

    def sign(self, message, private_key):
        x = private_key
        k = random.randint(1, self.q - 1)
        r = pow(self.g, k, self.p) % self.q
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        k_inv = mod_inverse(k, self.q)
        if k_inv is None:  # Check if modular inverse exists
            return None
        s = (k_inv * (h + x * r)) % self.q
        return (r, s)

    def verify(self, message, signature, public_key):
        r, s = signature
        y = public_key
        if r <= 0 or r >= self.q or s <= 0 or s >= self.q:
            return False
        w = mod_inverse(s, self.q)
        if w is None:  # Check if modular inverse exists
            return False
        h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
        u1 = (h * w) % self.q
        u2 = (r * w) % self.q
        v = ((pow(self.g, u1, self.p) * pow(y, u2, self.p)) % self.p) % self.q
        return v == r

# 示例使用
if __name__ == "__main__":
    dsa = DSA()
    
    # 生成密钥对
    private_key, public_key = dsa.generate_keypair()
    print(f"Private key: {private_key}")
    print(f"Public key: {public_key}")

    # 签名消息
    message = "Hello, Digital Signature Algorithm!"
    signature = dsa.sign(message, private_key)
    if signature is None:
        print("Failed to generate signature")
    else:
        print(f"Message: {message}")
        print(f"Signature: {signature}")

        # 验证签名
        is_valid = dsa.verify(message, signature, public_key)
        print(f"Signature is valid: {is_valid}")

        # 尝试验证被篡改的消息
        tampered_message = "Hello, Tampered Message!"
        is_valid = dsa.verify(tampered_message, signature, public_key)
        print(f"Tampered message signature is valid: {is_valid}")
