"""Minimal Keccak-256 + EIP-55 address validation.

Why this exists: an Ethereum receive address is irreversible. One wrong character
and every donation is burned permanently, with no way to notice from the website.
EIP-55 encodes a checksum in the letter casing of a mixed-case address, which
catches essentially any transposition or typo. Python's hashlib.sha3_256 is NOT
Keccak-256 (different padding byte), so the hash is implemented here.
No third party dependency, so the build stays dependency free.
"""
_RC = [0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,
       0x000000000000808B,0x0000000080000001,0x8000000080008081,0x8000000000008009,
       0x000000000000008A,0x0000000000000088,0x0000000080008009,0x000000008000000A,
       0x000000008000808B,0x800000000000008B,0x8000000000008089,0x8000000000008003,
       0x8000000000008002,0x8000000000000080,0x000000000000800A,0x800000008000000A,
       0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
_ROT = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
_M = (1 << 64) - 1

def _rotl(x, n): return ((x << n) | (x >> (64 - n))) & _M

def _keccak_f(A):
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ _rotl(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5): A[x][y] ^= D[x]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = _rotl(A[x][y], _ROT[x][y])
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & _M & B[(x + 2) % 5][y])
        A[0][0] ^= _RC[rnd]
    return A

def keccak256(data: bytes) -> bytes:
    rate = 136                                  # 1088 bits, Keccak-256
    data = bytearray(data)
    data.append(0x01)                           # Keccak padding, NOT SHA3's 0x06
    while len(data) % rate != 0: data.append(0x00)
    data[-1] ^= 0x80
    A = [[0] * 5 for _ in range(5)]
    for off in range(0, len(data), rate):
        blk = data[off:off + rate]
        for i in range(rate // 8):
            lane = int.from_bytes(blk[i * 8:(i + 1) * 8], 'little')
            A[i % 5][i // 5] ^= lane
        A = _keccak_f(A)
    out = b''.join(A[i % 5][i // 5].to_bytes(8, 'little') for i in range(4))
    return out[:32]

def to_checksum(addr: str) -> str:
    a = addr.lower().replace('0x', '')
    h = keccak256(a.encode()).hex()
    return '0x' + ''.join(c.upper() if c.isalpha() and int(h[i], 16) >= 8 else c
                          for i, c in enumerate(a))

def validate(addr: str):
    """Returns (ok, message). Rejects anything that is not a well formed,
    correctly checksummed, non burn address."""
    if not isinstance(addr, str) or not addr.startswith('0x') or len(addr) != 42:
        return False, 'must be 0x followed by exactly 40 hex characters'
    body = addr[2:]
    if any(c not in '0123456789abcdefABCDEF' for c in body):
        return False, 'contains a non hex character'
    if int(body, 16) == 0:
        return False, 'is the zero address, funds sent there are destroyed'
    if body.lower() == body or body.upper() == body:
        return False, ('is all one case, so it carries no EIP-55 checksum and a typo '
                       'cannot be detected. Re-copy the mixed case form from your wallet. '
                       f'Expected: {to_checksum(addr)}')
    if to_checksum(addr) != addr:
        return False, f'FAILS its EIP-55 checksum, so it is mistyped. Correct form would be {to_checksum(addr)}'
    return True, 'valid, EIP-55 checksum verified'
