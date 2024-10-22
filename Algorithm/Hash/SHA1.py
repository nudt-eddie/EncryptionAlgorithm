import struct

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha1(message):
    # 初始化哈希值
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # 预处理
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    while (len(message) + 8) % 64 != 0:
        message += b'\x00'
    message += struct.pack('>Q', original_bit_len)

    # 处理消息块
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        words = list(struct.unpack('>16I', chunk))

        # 扩展消息块
        for j in range(16, 80):
            words.append(left_rotate(words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16], 1))

        # 初始化哈希值
        a, b, c, d, e = h0, h1, h2, h3, h4

        # 主循环
        for j in range(80):
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + words[j]) & 0xffffffff
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # 更新哈希值
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    # 产生最终哈希值
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

# 示例使用
if __name__ == "__main__":
    message = "Hello, SHA-1!"
    print(f"Message: {message}")
    print(f"SHA-1 Hash: {sha1(message.encode('utf-8'))}")
