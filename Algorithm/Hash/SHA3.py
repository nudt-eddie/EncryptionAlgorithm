import math

# SHA-3 (Keccak) constants
KECCAK_ROUNDS = 24
KECCAK_STATE_SIZE = 1600

# Round constants
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

def keccak_f(state):
    def rol(x, s):
        return ((x << s) | (x >> (64 - s))) & 0xFFFFFFFFFFFFFFFF

    def round(A, RC):
        # θ step
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x + 4) % 5] ^ rol(C[(x + 1) % 5], 1) for x in range(5)]
        A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]

        # ρ and π steps
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2*x + 3*y) % 5] = rol(A[x][y], ((x + 1) * (x + 2) // 2) % 64)

        # χ step
        A = [[B[x][y] ^ ((~B[(x+1) % 5][y]) & B[(x+2) % 5][y]) for y in range(5)] for x in range(5)]

        # ι step
        A[0][0] ^= RC
        return A

    lanes = [[state[8*(x + 5*y):8*(x + 5*y) + 8] for y in range(5)] for x in range(5)]
    A = [[int.from_bytes(lanes[x][y], 'little') for y in range(5)] for x in range(5)]

    for i in range(KECCAK_ROUNDS):
        A = round(A, RC[i])

    state = b''.join(b''.join(x.to_bytes(8, 'little') for x in row) for row in A)
    return state

def sha3_256(message):
    rate = 1088
    capacity = 512
    suffix = 0x06

    # Padding
    padded = bytearray(message)
    padded.append(suffix)
    padded.extend(b'\x00' * (-len(padded) % (rate // 8)))
    padded[-1] |= 0x80

    # Initialize state
    state = bytearray(KECCAK_STATE_SIZE // 8)

    # Absorbing phase
    for i in range(0, len(padded), rate // 8):
        block = padded[i:i + rate // 8]
        for j in range(len(block)):
            state[j] ^= block[j]
        state = keccak_f(state)

    # Squeezing phase
    output = bytearray()
    output_length = 256 // 8
    while len(output) < output_length:
        output.extend(state[:rate // 8])
        state = keccak_f(state)

    return output[:output_length].hex()

# 示例使用
if __name__ == "__main__":
    message = "Hello, SHA-3!"
    print(f"Message: {message}")
    print(f"SHA3-256 Hash: {sha3_256(message.encode())}")
