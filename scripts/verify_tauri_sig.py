"""Verify Tauri updater minisign signatures without third-party modules.

Derived from RelayHub's verify_sig.py. The public key is embedded; both the
file signature and trusted-comment signature must verify.
"""

import argparse
import base64
import binascii
import hashlib
import json
from pathlib import Path
import sys

PUBLIC_KEY = "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IEE4OTY3MzJGRjAwOUU0RUYKUldUdjVBbndMM09XcUlJSnAzck5YWG9KdVZIUFk3STlzM1ErUC8vTGk1Y2g1c3U3U2Z4TnBLZlIK"

p = 2 ** 255 - 19
q = 2 ** 252 + 27742317777372353535851937790883648493
d = -121665 * pow(121666, p - 2, p) % p
SQRT_M1 = pow(2, (p - 1) // 4, p)


def _add(P, Q):
    a = (P[1] - P[0]) * (Q[1] - Q[0]) % p
    b = (P[1] + P[0]) * (Q[1] + Q[0]) % p
    c = 2 * P[3] * Q[3] * d % p
    e = 2 * P[2] * Q[2] % p
    E, F, G, H = b - a, e - c, e + c, b + a
    return (E * F % p, G * H % p, F * G % p, E * H % p)


def _mul(s, P):
    R = (0, 1, 1, 0)
    while s:
        if s & 1:
            R = _add(R, P)
        P = _add(P, P)
        s >>= 1
    return R


def _equal(P, Q):
    return (P[0] * Q[2] - Q[0] * P[2]) % p == 0 and (P[1] * Q[2] - Q[1] * P[2]) % p == 0


def _recover_x(y, sign):
    if y >= p:
        return None
    x2 = (y * y - 1) * pow(d * y * y + 1, p - 2, p) % p
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (p + 3) // 8, p)
    if (x * x - x2) % p:
        x = x * SQRT_M1 % p
    if (x * x - x2) % p:
        return None
    return p - x if (x & 1) != sign else x


def _decompress(s):
    y = int.from_bytes(s, 'little')
    sign, y = y >> 255, y & ((1 << 255) - 1)
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % p)


_GY = 4 * pow(5, p - 2, p) % p
_GX = _recover_x(_GY, 0)
BASE = (_GX, _GY, 1, _GX * _GY % p)


def ed25519_verify(public, msg, sig):
    if len(public) != 32 or len(sig) != 64:
        return False
    A, R = _decompress(public), _decompress(sig[:32])
    s = int.from_bytes(sig[32:], 'little')
    if A is None or R is None or s >= q:
        return False
    h = int.from_bytes(hashlib.sha512(sig[:32] + public + msg).digest(), 'little') % q
    return _equal(_mul(s, BASE), _add(R, _mul(h, A)))


def _lines(b64_text):
    return base64.b64decode(b64_text.strip(), validate=True).decode('utf-8').splitlines()


def load_pubkey():
    lines = _lines(PUBLIC_KEY)
    if len(lines) != 2:
        raise ValueError('invalid public key format')
    raw = base64.b64decode(lines[1], validate=True)
    if len(raw) != 42 or raw[:2] != b'Ed':
        raise ValueError('invalid minisign public key')
    return raw[2:10], raw[10:]


def verify(path, sig_path):
    key_id, public = load_pubkey()
    lines = _lines(Path(sig_path).read_text(encoding='utf-8'))
    if len(lines) != 4 or not lines[2].startswith('trusted comment: '):
        raise ValueError('invalid signature format')
    raw = base64.b64decode(lines[1], validate=True)
    comment_sig = base64.b64decode(lines[3], validate=True)
    if len(raw) != 74 or raw[:2] not in (b'ED', b'Ed') or len(comment_sig) != 64:
        raise ValueError('invalid signature encoding or algorithm')
    alg, sig_key_id, sig = raw[:2], raw[2:10], raw[10:]
    trusted = lines[2][len('trusted comment: '):]
    data = Path(path).read_bytes()
    msg = hashlib.blake2b(data, digest_size=64).digest() if alg == b'ED' else data
    return {
        'file': str(path),
        'file_sha256': hashlib.sha256(data).hexdigest(),
        'algorithm': alg.decode('ascii'),
        'key_id_matches': sig_key_id == key_id,
        'file_signature_valid': sig_key_id == key_id and ed25519_verify(public, msg, sig),
        'trusted_comment_valid': ed25519_verify(public, sig + trusted.encode('utf-8'), comment_sig),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--sig', type=Path)
    args = parser.parse_args(argv)
    try:
        result = verify(args.file, args.sig or args.file.with_name(args.file.name + '.sig'))
    except (OSError, UnicodeError, ValueError, IndexError, binascii.Error):
        print('验签失败：文件或签名格式无效。', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['file_signature_valid'] and result['trusted_comment_valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
