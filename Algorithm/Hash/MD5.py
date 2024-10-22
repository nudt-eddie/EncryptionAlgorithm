import struct
from math import sin
from enum import Enum

class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

class MD5:
    def __init__(self): 
        self.buffers = {
            MD5Buffer.A: MD5Buffer.A.value,
            MD5Buffer.B: MD5Buffer.B.value,
            MD5Buffer.C: MD5Buffer.C.value,
            MD5Buffer.D: MD5Buffer.D.value
        }
        self.functions = [self._f, self._g, self._h, self._i]
        self.rotate_amounts = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

    def _f(self, b, c, d):
        return (b & c) | (~b & d)

    def _g(self, b, c, d):
        return (b & d) | (c & ~d)

    def _h(self, b, c, d):
        return b ^ c ^ d

    def _i(self, b, c, d):
        return c ^ (b | ~d)

    def _leftrotate(self, x, c):
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

    def _process_chunk(self, chunk):
        w = list(struct.unpack('<16I', chunk))
        a, b, c, d = [self.buffers[buffer] for buffer in MD5Buffer]

        for i in range(64):
            f = self.functions[i // 16]
            g = (i * 3 + 1) % 16 if i // 16 == 1 else \
                (i * 5 + 1) % 16 if i // 16 == 2 else \
                i % 16 if i // 16 == 3 else \
                i

            temp = d
            d = c
            c = b
            k = int(abs(sin(i + 1)) * 2**32)
            b = (b + self._leftrotate((a + f(b, c, d) + w[g] + k) & 0xFFFFFFFF, self.rotate_amounts[i])) & 0xFFFFFFFF
            a = temp

        for buffer, val in zip(MD5Buffer, [a, b, c, d]):
            self.buffers[buffer] = (self.buffers[buffer] + val) & 0xFFFFFFFF

    def md5(self, message):
        message = bytearray(message, 'ascii')
        orig_len_in_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += struct.pack('<Q', orig_len_in_bits)

        for chunk in range(0, len(message), 64):
            self._process_chunk(message[chunk:chunk+64])

        return struct.pack('<4I', *(self.buffers[buffer] for buffer in MD5Buffer))

    def hexdigest(self, message):
        return self.md5(message).hex()

# 示例使用
if __name__ == "__main__":
    md5 = MD5()
    message = "Hello, MD5!"
    print(f"Message: {message}")
    print(f"MD5 Hash: {md5.hexdigest(message)}")
