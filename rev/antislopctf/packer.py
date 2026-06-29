import struct

def fnv1a(name):
    h = 0x811C9DC5
    for c in name:
        b = ord(c)
        if ord('A') <= b <= ord('Z'):
            b += 32
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return h

def xor_name(name, kind):
    key = 23 * kind + 65
    out = bytearray()
    for b in name.encode():
        out.append((key ^ b) & 0xFF)
        key += 17
    return bytes(out)

def xor_data(data, kind):
    base, counter, out = (19 * kind) ^ 0xA7, 0, bytearray()
    for b in data:
        out.append((base ^ counter ^ b) & 0xFF)
        counter = (counter + 29) & 0xFF
    return bytes(out)

def build_glyp(entries):
    entries = sorted(entries, key=lambda e: fnv1a(e[0]))
    header = b'GLYP' + bytes([1, len(entries), 0, 0])
    body = b''
    for name, data, kind in entries:
        enc_name = xor_name(name, kind)
        enc_data = xor_data(data, kind)
        body += fnv1a(name).to_bytes(4, 'little')
        body += len(enc_name).to_bytes(2, 'little')
        body += len(enc_data).to_bytes(4, 'little')
        body += bytes([kind])
        body += enc_name + enc_data
    return header + body
